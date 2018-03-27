# ZeroMQ sleep test

Code used for testing `keepalive` settings on DC/OS ([Jira ticket DCOS_OSS-1591](https://jira.mesosphere.com/browse/DCOS_OSS-1591)).

By defining ENV variable `TCP_KEEPALIVE_IDLE=1000` on subscriber task you can experiment with `keepalive` (in seconds) for you OS.

## Marathon tasks

Publisher configuration:
```json
{
  "id": "/zmq/pub",
  "backoffFactor": 1.15,
  "backoffSeconds": 1,
  "cmd": "python3 pub.py -v",
  "container": {
    "portMappings": [
      {
        "containerPort": 6500,
        "hostPort": 0,
        "labels": {
          "VIP_0": "/zmq/pub:6500"
        },
        "protocol": "tcp",
        "servicePort": 10123,
        "name": "pub"
      }
    ],
    "type": "DOCKER",
    "volumes": [],
    "docker": {
      "image": "deric/pub-sub-sleep:latest",
      "forcePullImage": false,
      "privileged": false,
      "parameters": []
    }
  },
  "cpus": 0.1,
  "disk": 0,
  "instances": 1,
  "maxLaunchDelaySeconds": 3600,
  "mem": 128,
  "gpus": 0,
  "networks": [
    {
      "mode": "container/bridge"
    }
  ],
  "requirePorts": false,
  "upgradeStrategy": {
    "maximumOverCapacity": 1,
    "minimumHealthCapacity": 1
  },
  "killSelection": "YOUNGEST_FIRST",
  "unreachableStrategy": {
    "inactiveAfterSeconds": 0,
    "expungeAfterSeconds": 0
  },
  "healthChecks": [],
  "fetch": [],
  "constraints": []
}
```

and subscriber:
```json
{
  "id": "/zmq/sub",
  "backoffFactor": 1.15,
  "backoffSeconds": 1,
  "cmd": "python3 sub.py --host tcp://zmqpub.marathon.l4lb.thisdcos.directory:6500",
  "container": {
    "type": "DOCKER",
    "volumes": [],
    "docker": {
      "image": "deric/pub-sub-sleep:latest",
      "forcePullImage": true,
      "privileged": false,
      "parameters": []
    }
  },
  "cpus": 0.1,
  "disk": 0,
  "env": {  },
  "instances": 1,
  "maxLaunchDelaySeconds": 3600,
  "mem": 128,
  "gpus": 0,
  "networks": [
    {
      "mode": "host"
    }
  ],
  "portDefinitions": [],
  "requirePorts": false,
  "upgradeStrategy": {
    "maximumOverCapacity": 1,
    "minimumHealthCapacity": 1
  },
  "killSelection": "YOUNGEST_FIRST",
  "unreachableStrategy": {
    "inactiveAfterSeconds": 0,
    "expungeAfterSeconds": 0
  },
  "healthChecks": [],
  "fetch": [],
  "constraints": []
}
```
