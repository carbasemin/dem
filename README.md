# Docker Event Monitor (DEM)

### What is it?
A tiny container that monitors the local Docker event system in real-time and sends out notifications to various integrations for event types that match the configuration.

For example, you can trigger an alert when a container is stopped, killed, runs out of memory or health status change.

For a full list of events that are supported see the official [Docker Documentation](https://docs.docker.com/engine/reference/commandline/events/).

### Features
- Integrations for **Slack**, **Discord**, **Sparkpost** and **Alertmanager**.
- Super light-weight container requrements (< 20MB Memory, < 100MB uncompressed image size).
- Customisable event triggers.
- No exposed ports.

### Quick Start
Pull [the image](https://hub.docker.com/r/carbasemin/dem) and run the container on the host you want to monitor mounting in the `docker.sock` and `conf.yml` file:

```
docker run -d --name dem \
-v /var/run/docker.sock:/var/run/docker.sock \
-v conf.yml:/app/conf.yml \
carbasemin/dem:latest
```
### Configuration
Example `conf.yml` with a subset of available event types that will trigger a notification. For a full list of all available event types please see the official [Docker Documentation](https://docs.docker.com/engine/reference/commandline/events/).

```
settings:
  logging: info ## Log verbosity <debug, info (default), warn, error>
  tags: ## List of tags you want to appear in notifications for identification purposes
    - production
    - example one
  exclusions: ## The name of any actors (containers, networks etc) you want to exclude from alerts
    - foo
  inclusions: ## If specified, only events from these actors will be alerted on. Any actors not in this list are implicitly excluded, therefore this is mutually exclusive with the above `exclusions` option.
    - foo
  silence: ## Time window where alerts will be silenced
    start: "02:00" ## Start of the silence window in 24 hour format
    duration: 120 ## Duration in minutes for the window to last
    exclusions: ## The name of any actors (containers, networks etc) you want to exclude from the silence window
      - foo
    inclusions: ## If specified, only events from these actors will be included in the silence window. Any actors not in this list are implicitly excluded, therefore this is mutually exclusive with the above `exclusions` option.
      - foo

events: ## The Docker event types that you want to trigger alerts for
  container: 
    - 'health_status: unhealthy'
    - oom
    - destroy
    - create
  image: 
    - delete
  plugin:
    - install
    - remove
  volume: 
    - destroy
    - create
  network:
    - destroy
  daemon:
    - reload
  service:
    - remove
  node:
    - remove
  secret:
    - remove
  config:
    - remove

integrations: ## Available integrations  
  slack:
    enabled: True
    url: https://hooks.slack.com/services/<your_uuid>
  sparkpost:
    enabled: True
    url: https://api.eu.sparkpost.com/api/v1/transmissions
    key: your_key
    from: dem@dkrmon.io
    subject: Docker Event Monitor
    recipients:
      - john.smith@example.com
      - mary.collins@example.com
  discord:
    enabled: True
    url: https://discordapp.com/api/webhooks/<your_uuid>
  alertmanager:
    enabled: True
    url: http://alertmanager/api/v1/alerts
    basic_auth:
      username: admin 
      password: test
```

### Integrations
#### Slack
To configure DEM to work with Slack you will need to create a web-hook from your Slack administration panel which will provide you with the unique URL to add to your DEM configuration. Please see the official [Slack documentation](https://get.slack.help/hc/en-us/articles/115005265063-Incoming-webhooks-for-Slack).

#### Discord
To configure DEM to work with Discord you will need to create a webhook from Discord which will provide you with the unique URL to add to your DEM configuration. Please see the official [Discord documentation](https://support.discordapp.com/hc/en-us/articles/228383668-Intro-to-Webhooks).

#### SparkPost
To configure DEM to work with SparkPost you will need to generate an API key from your SparkPost dashboard with the following minimal credentials: `Templates: Read-only`, `Transmissions: Read/Write`, `Send via SMTP`. You can then and add the key to your DEM configuration along with the `from` address, `subject` and any `recipients` you want the emails to be sent to. For setting up API keys, please see the official [SparkPost documentation](https://www.sparkpost.com/docs/getting-started/create-api-keys/).

The `url` will either be `https://api.sparkpost.com/api/v1/transmissions` for non EU accounts and `https://api.eu.sparkpost.com/api/v1/transmissions` for EU accounts. These are subject to change so please check the [SparkPost documentation](https://developers.sparkpost.com/api/#header-endpoints).

#### Alertmanager
For now, just provide a URL, e.g., `192.168.X.X:9093/api/v1/alerts` to speak with an Alertmanager container running locally. HTTP basic auth is supported now.

Additionaly, you may want to use something like `resolve_timeout=3s` in Alertmanager config since these alerts don't have a meaningful resolution to them. But if you don't specify a `resolve_timeout`, the alerts just stay in Alertmanager for hours (the default resolve timeout amount). After that, you could use `send_resolved=False` to not send an alert for meaningles resolved alerts.
