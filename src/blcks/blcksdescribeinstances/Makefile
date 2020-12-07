.PHONY: pre-build

pre-build:
	mkdir -p template && \
	ofsm template -l python3_blcks_flask template && \
	faas-cli build --name=blcksdescribeinstances --lang=python3_blcks_flask --image=blcksdescribeinstances --handler=handler --shrinkwrap && \
	cp *.para build/blcksdescribeinstances