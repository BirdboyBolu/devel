#!/bin/bash

test_name="$1"

rm -rf logs/$test_name
mkdir logs/$test_name

allnodesfile="allnodes"
rm -rf $allnodesfile

echo "$test_name" | python -c "import json,sys; tst=sys.stdin.read().strip(); containers=json.loads(open('tests/%s/conf.json' % tst).read())['containers'].keys(); open('allnodes', 'w').write(' '.join(containers));"

nodes=`cat $allnodesfile`

for node in $nodes; do
    echo "[$node]";
    docker-compose --file tests/$test_name/docker-compose.yml exec -T $node sh -c "cd /root/.bitdust/logs/; tar cf logs.tar *; cat logs.tar" 1> logs/$test_name/$node.tar 2>/dev/null;
#     docker-compose --file tests/$test_name/docker-compose.yml exec -T $node sh -c "cat /root/.bitdust/logs/automats.log" 1> logs/$test_name/automats.$node.log 2>/dev/null;
#     docker-compose --file tests/$test_name/docker-compose.yml exec -T $node sh -c "cat /root/.bitdust/logs/api.log" 1> logs/$test_name/api.$node.log 2>/dev/null;
#     docker-compose --file tests/$test_name/docker-compose.yml exec -T $node sh -c "cat /root/.bitdust/logs/event.log" 1> logs/$test_name/event.$node.log 2>/dev/null;
#     docker-compose --file tests/$test_name/docker-compose.yml exec -T $node sh -c "cat /root/.bitdust/logs/packet.log" 1> logs/$test_name/packet.$node.log 2>/dev/null;
#     docker-compose --file tests/$test_name/docker-compose.yml exec -T $node sh -c "cat /root/.bitdust/logs/stdout.log" 1> logs/$test_name/stdout.$node.log 2>/dev/null;
#     docker-compose --file tests/$test_name/docker-compose.yml exec -T $node sh -c "cat /root/.bitdust/logs/err.log" 1> logs/$test_name/err.$node.log 2>/dev/null;
#     docker-compose --file tests/$test_name/docker-compose.yml exec -T $node sh -c "cat /root/.bitdust/logs/main.log" 1> logs/$test_name/main.$node.log 2>/dev/null;
#     docker-compose --file tests/$test_name/docker-compose.yml exec -T $node sh -c "cat /root/.bitdust/logs/warn.log" 1> logs/$test_name/warn.$node.log 2>/dev/null;
#     docker-compose --file tests/$test_name/docker-compose.yml exec -T $node sh -c "cat /root/.bitdust/logs/exception_*.log" 1> logs/$test_name/exception.$node.log 2>/dev/null;
done

rm -rf $allnodesfile
