# Issues

1. fix

    - check the cluster health

        ```json
        curl localhost:9200/_cluster/health?pretty
        {
        "cluster_name": "my_cluster",
        "status": "red",
        "timed_out": false,
        "number_of_nodes": 5,
        "number_of_data_nodes": 5,
        "active_primary_shards": 16037,
        "active_shards": 20808,
        "relocating_shards": 0,
        "initializing_shards": 0,
        "unassigned_shards": 11422,
        "delayed_unassigned_shards": 0,
        "number_of_pending_tasks": 0,
        "number_of_in_flight_fetch": 0,
        "task_max_waiting_in_queue_millis": 0,
        "active_shards_percent_as_number": 64.5609680421967
        }
        ```

        so many unassigned_shards existed
    - re-shards with

        ```sh
        curl -X PUT "localhost:9200/_cluster/settings?pretty" -H 'Content-Type: application/json' -d'
        {
            "transient" : {
                "cluster.routing.allocation.enable" : "all"
            }
        }
        '
        ```

    - if still not working, try

        ```sh
        curl -H 'Content-Type: application/json' -X POST -d '' localhost:9200/_cluster/reroute?retry_failed
        ```

        then you will see re-sharding is on going.
