# miniflux


## feeds


## configuration(configure database)
- check user_id, here I only have
```
miniflux=> select id,username from users ;
 id | username
----+-----------
  1 | jenningsl
(1 row)
```
- enable crawler all content
```
miniflux=> UPDATE feeds SET crawler='t' WHERE user_id = 1;
UPDATE 63
```

- enable fetch_via_proxy
```
miniflux=> UPDATE feeds SET fetch_via_proxy='1' WHERE user_id = 1;
UPDATE 63
```
