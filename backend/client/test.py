import docker

client = docker.DockerClient(
    base_url="npipe:////./pipe/docker_engine"
)

print("Ping:", client.ping())

for c in client.containers.list(all=True):
    print(c.name, c.status)