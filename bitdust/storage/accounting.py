#!/usr/bin/python
# accouning.py
#
# Copyright (C) 2008 Veselin Penev, https://bitdust.io
#
# This file (accounting.py) is part of BitDust Software.
#
# BitDust is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# BitDust Software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with BitDust Software.  If not, see <http://www.gnu.org/licenses/>.
#
# Please contact us if you have any questions at bitdust.io@gmail.com
#
#
#
#
"""
.. module:: accouning.

Various methods to keep track of:

    + donated space
    + needed space
    + used space
    + free space
    + consumed space
"""

#------------------------------------------------------------------------------

from __future__ import absolute_import

#------------------------------------------------------------------------------

_Debug = False
_DebugLevel = 4

#------------------------------------------------------------------------------

import os
import math

from bitdust.logs import lg

from bitdust.system import bpio
from bitdust.system import diskusage

from bitdust.lib import misc
from bitdust.lib import strng
from bitdust.lib import jsn

from bitdust.main import settings

from bitdust.contacts import contactsdb

from bitdust.userid import id_url

from bitdust.storage import backup_fs

#------------------------------------------------------------------------------


def init():
    if _Debug:
        lg.out(_DebugLevel, 'accounting.init')


#------------------------------------------------------------------------------


def read_customers_quotas():
    space_dict = bpio._read_dict(settings.CustomersSpaceFile(), {})
    free_space = int(space_dict.pop('free', 0))
    space_dict = {id_url.field(k).to_bin(): v for k, v in space_dict.items()}
    return space_dict, free_space


def write_customers_quotas(new_space_dict, free_space):
    space_dict = {id_url.field(k).to_text(): v for k, v in new_space_dict.items()}
    space_dict['free'] = free_space
    return bpio._write_dict(settings.CustomersSpaceFile(), space_dict)


def get_customer_quota(customer_idurl):
    customer_idurl = id_url.field(customer_idurl).to_bin()
    try:
        return int(read_customers_quotas()[0].get(customer_idurl, None))
    except:
        return None


def check_create_customers_quotas(donated_bytes=None):
    if not os.path.isfile(settings.CustomersSpaceFile()):
        bpio._write_dict(settings.CustomersSpaceFile(), {
            'free': donated_bytes or settings.getDonatedBytes(),
        })
        lg.info('created a new customers quotas file: %s' % settings.CustomersSpaceFile())
        return True
    return False


def count_consumed_space(space_dict=None):
    if space_dict is None:
        space_dict = read_customers_quotas()[0]
    consumed_bytes = 0
    for idurl, customer_consumed in space_dict.items():
        consumed_bytes += int(customer_consumed)
    return consumed_bytes


def validate_customers_quotas(space_dict=None, free_space=None):
    unknown_customers = set()
    unused_quotas = set()
    if space_dict is None or free_space is None:
        space_dict, free_space = read_customers_quotas()
    for idurl in list(space_dict.keys()):
        idurl = strng.to_bin(idurl)
        try:
            space_dict[idurl] = int(space_dict[idurl])
        except:
            unknown_customers.add(idurl)
            continue
        if space_dict[idurl] <= 0:
            unknown_customers.add(idurl)
            continue
    for idurl in contactsdb.customers():
        if idurl.to_bin() not in list(space_dict.keys()):
            unknown_customers.add(idurl)
    for idurl in space_dict.keys():
        if idurl not in id_url.to_bin_list(contactsdb.customers()):
            unused_quotas.add(idurl)
    return unknown_customers, unused_quotas


#------------------------------------------------------------------------------


def read_customers_usage():
    usage_dict = jsn.dict_keys_to_bin(bpio._read_dict(settings.CustomersUsedSpaceFile(), {}))
    usage_dict = {id_url.field(k).to_bin(): v for k, v in usage_dict.items()}
    return usage_dict


def update_customers_usage(new_space_usage_dict):
    usage_dict = {id_url.field(k).to_bin(): v for k, v in new_space_usage_dict.items()}
    return bpio._write_dict(settings.CustomersUsedSpaceFile(), jsn.dict_keys_to_text(usage_dict))


def calculate_customers_usage_ratio(space_dict=None, used_dict=None):
    if space_dict is None:
        space_dict, _ = read_customers_quotas()
    if used_dict is None:
        used_dict = read_customers_usage()
    current_customers = contactsdb.customers()
    used_space_ratio_dict = {}
    for idurl in current_customers:
        allocated_bytes = int(space_dict[idurl.to_bin()])
        try:
            files_size = int(used_dict.get(idurl.to_bin(), 0))
        except:
            lg.exc()
            files_size = 0
        try:
            ratio = float(files_size)/float(allocated_bytes)
        except:
            lg.exc()
            continue
        used_space_ratio_dict[idurl.to_bin()] = ratio
    return used_space_ratio_dict


#------------------------------------------------------------------------------


def report_consumed_storage():
    result = {}
    result['suppliers_num'] = contactsdb.num_suppliers()
    result['needed'] = settings.getNeededBytes()
    # result['needed_str'] = diskspace.MakeStringFromBytes(result['needed'])
    result['used'] = int(backup_fs.sizebackups()/2)
    # result['used_str'] = diskspace.MakeStringFromBytes(result['used'])
    result['available'] = result['needed'] - result['used']
    # result['available_str'] = diskspace.MakeStringFromBytes(result['available'])
    result['needed_per_supplier'] = 0
    result['used_per_supplier'] = 0
    result['available_per_supplier'] = 0
    if result['suppliers_num'] > 0:
        result['needed_per_supplier'] = int(math.ceil(2.0*result['needed']/result['suppliers_num']))
        result['used_per_supplier'] = int(math.ceil(2.0*result['used']/result['suppliers_num']))
        result['available_per_supplier'] = result['needed_per_supplier'] - result['used_per_supplier']
    # result['needed_per_supplier_str'] = diskspace.MakeStringFromBytes(result['needed_per_supplier'])
    # result['used_per_supplier_str'] = diskspace.MakeStringFromBytes(result['used_per_supplier'])
    # result['available_per_supplier_str'] = diskspace.MakeStringFromBytes(result['available_per_supplier'])
    try:
        result['used_percent'] = misc.value2percent(float(result['used']), float(result['needed']))
    except:
        result['used_percent'] = '0%'
    return result


def report_donated_storage():
    space_dict, free_space = read_customers_quotas()
    used_space_dict = read_customers_usage()
    r = {}
    r['customers_num'] = contactsdb.num_customers()
    r['customers'] = []
    r['old_customers'] = []
    r['errors'] = []
    r['consumed'] = 0
    r['donated'] = settings.getDonatedBytes()
    # r['donated_str'] = diskspace.MakeStringFromBytes(r['donated'])
    r['real'] = bpio.getDirectorySize(settings.getCustomersFilesDir())
    try:
        r['free'] = int(free_space)
    except:
        r['free'] = 0
    used = 0
    for idurl in id_url.to_bin_list(contactsdb.customers()):
        consumed_by_customer = 0
        used_by_customer = 0
        if idurl not in list(space_dict.keys()):
            r['errors'].append('space consumed by customer %r is unknown' % idurl)
        else:
            try:
                consumed_by_customer = int(space_dict.pop(idurl))
                r['consumed'] += consumed_by_customer
            except:
                r['errors'].append('incorrect value of consumed space for customer %r' % idurl)
                continue
        if idurl in list(used_space_dict.keys()):
            try:
                used_by_customer = int(used_space_dict.pop(idurl))
                used += used_by_customer
            except:
                r['errors'].append('incorrect value of used space for customer %r' % idurl)
                continue
        if consumed_by_customer < used_by_customer:
            r['errors'].append('customer %r currently using more space than requested' % idurl)
        c = {}
        c['idurl'] = strng.to_text(idurl)
        c['used'] = used_by_customer
        # c['used_str'] = diskspace.MakeStringFromBytes(c['used'])
        c['consumed'] = consumed_by_customer
        # c['consumed_str'] = diskspace.MakeStringFromBytes(c['consumed'])
        c['real'] = bpio.getDirectorySize(settings.getCustomerFilesDir(idurl))
        # c['real_str'] = diskspace.MakeStringFromBytes(c['real'])
        r['customers'].append(c)
    r['used'] = used
    # r['used_str'] = diskspace.MakeStringFromBytes(r['used'])
    # r['consumed_str'] = diskspace.MakeStringFromBytes(r['consumed'])
    if r['donated'] != r['free'] + r['consumed']:
        r['errors'].append('total consumed %d and known free %d (%d total) bytes not match with donated %d bytes' % (r['consumed'], r['free'], r['consumed'] + r['free'], r['donated']))
    if r['used'] > r['donated']:
        r['errors'].append('total space used by customers exceed the donated limit')
    if len(space_dict) > 0:
        r['errors'].append('found %d incorrect records of consumed space' % len(space_dict))
    if r['real'] != r['used']:
        r['errors'].append('current info needs update, known size is %d bytes but real is %d bytes' % (r['used'], r['real']))
    old_customers_used = 0
    old_customers_real = 0
    for idurl in used_space_dict.keys():
        real = bpio.getDirectorySize(settings.getCustomerFilesDir(idurl))
        try:
            used = int(used_space_dict[idurl])
        except:
            r['errors'].append('incorrect value of used space for customer %r' % idurl)
            continue
        r['old_customers'].append({
            'idurl': strng.to_text(idurl),
            'used': used,  # 'used_str': diskspace.MakeStringFromBytes(used_space_dict[idurl]),
            'real': real,  # 'real_str': diskspace.MakeStringFromBytes(real),
        })
        old_customers_used += used
        old_customers_real += real
    r['old_customers_used'] = old_customers_used
    r['old_customers_real'] = old_customers_real
    try:
        r['used_percent'] = misc.value2percent(float(r['used']), float(r['donated']), 5)
    except:
        r['used_percent'] = ''
    try:
        r['consumed_percent'] = misc.value2percent(float(r['consumed']), float(r['donated']), 5)
    except:
        r['consumed_percent'] = ''
    return r


def report_local_storage():
    # TODO
    # if customers folder placed outside of BaseDir()
    # need to add: total = total + customers
    r = {}
    r['backups'] = bpio.getDirectorySize(settings.getLocalBackupsDir())
    # r['backups_str'] = diskspace.MakeStringFromBytes(r['backups'])
    r['temp'] = bpio.getDirectorySize(settings.getTempDir())
    # r['temp_str'] = diskspace.MakeStringFromBytes(r['temp'])
    r['customers'] = bpio.getDirectorySize(settings.getCustomersFilesDir())
    # r['customers_str'] = diskspace.MakeStringFromBytes(r['customers'])
    r['total'] = bpio.getDirectorySize(settings.AppDataDir())
    # r['total_str'] = diskspace.MakeStringFromBytes(r['total'])
    dataDriveFreeSpace, dataDriveTotalSpace = diskusage.GetDriveSpace(settings.getCustomersFilesDir())
    if dataDriveFreeSpace is None:
        dataDriveFreeSpace = 0
    r['disktotal'] = int(dataDriveTotalSpace)
    # r['disktotal_str'] = diskspace.MakeStringFromBytes(r['disktotal'])
    r['diskfree'] = int(dataDriveFreeSpace)
    # r['diskfree_str'] = diskspace.MakeStringFromBytes(r['diskfree'])
    try:
        r['total_percent'] = misc.value2percent(float(r['total']), float(r['disktotal']), 5)
    except:
        r['total_percent'] = ''
    try:
        r['diskfree_percent'] = misc.value2percent(float(r['diskfree']), float(r['disktotal']), 5)
    except:
        r['diskfree_percent'] = ''
    return r
