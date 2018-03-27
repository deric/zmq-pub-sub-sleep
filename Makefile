NAME=deric/pub-sub-sleep

all: release

remote:
	git push

build:
	docker pull python:3.6-slim-stretch
	docker build -t $(NAME) .

pub: build
	docker run -i -t $(NAME) python3 pub.py --host $(ip addr show eth0)

sub: build
	docker run -i -t $(NAME) python3 sub.py

bash:
	docker run --entrypoint /bin/bash -it $(NAME)

clean:
	docker rm `docker ps -aq`

define RELEASE
	git pull
	git push
	git tag "v$(1)"
	git push origin --tags
	docker tag $(NAME) $(NAME):$(1)
	docker tag $(NAME) $(NAME):latest
	docker push $(NAME)
endef

release: build
	$(call RELEASE,$(v))

push:
	docker push $(REGISTRY)/$(NAME)
