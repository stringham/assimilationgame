#######################################
# Makefile-specific variables         #
#######################################

SHELL = /bin/bash -e
MAKEFLAGS = -j 4

#######################################
# Other Variables                     #
#######################################

CALCDEPS := assimilation/static/js/closure/closure/bin/calcdeps.py
CLOSUREBUILDER := assimilation/static/js/closure/closure/bin/build/closurebuilder.py
COMPILED_JS_SOURCES = $(shell find assimilation/static/js/app -type f -name "*.js")

LESSC := tools/less/bin/lessc
LESS_FILES := $(shell find assimilation/static/css/ -name "*.less")
LESS_CSS_SOURCES := $(shell find assimilation/static/css/ -name "*.less" -a -not -name "_*.less")
LESS_CSS_COMPILED := $(subst .less,.css,$(LESS_CSS_SOURCES))


#######################################
# Common Targets                      #
#######################################

.DELETE_ON_ERROR:
.DEFAULT: help

.PHONY: help
help:
	@echo "### MAKE TARGETS ###"
	@echo "  help                    Print this help"
	@echo "  js                      Run both app and client targets"
	@echo "  app                     Compile the JavaScript sources to create the minified and optimized app.js"
	@echo "  css                     Less CSS Compiler"
	@echo "  deps                    Generate the JavaScript dependency file"
	@echo "  clean                   Clean all targets"
	@echo "  clean-js                Clean js target"
	@echo "  clean-app               Clean app target"
	@echo "  clean-css               Clean CSS"
	@echo "  clean-deps              Clean deps target"
	@echo "  run                     Run the server"

.PHONY: clean
clean: clean-js clean-css clean-deps


#######################################
# JS (closure) Functions              #
#######################################

# compilejs
# Compiles an application file
#
# $(1) = intermediate file prefix (source-map, var-map)
# $(2) = application file(s)
# $(3) = output file
compilejs = $(CLOSUREBUILDER)                                                        \
            --root=assimilation/static/js                                            \
            $(foreach app,$(2),-i $(app))                                            \
            -o compiled                                                              \
            -c tools/compiler/compiler.jar                                           \
            -f "--compilation_level=ADVANCED_OPTIMIZATIONS"                          \
            -f "--externs=assimilation/static/js/app/externs.js"                     \
            -f "--warning_level=VERBOSE"                                             \
            -f "--jscomp_error=accessControls"                                       \
            -f "--jscomp_error=checkRegExp"                                          \
            -f "--jscomp_error=checkTypes"                                           \
            -f "--jscomp_error=checkVars"                                            \
            -f "--jscomp_error=deprecated"                                           \
            -f "--jscomp_error=fileoverviewTags"                                     \
            -f "--jscomp_error=invalidCasts"                                         \
            -f "--jscomp_error=missingProperties"                                    \
            -f "--jscomp_error=nonStandardJsDocs"                                    \
            -f "--jscomp_error=strictModuleDepCheck"                                 \
            -f "--jscomp_error=undefinedVars"                                        \
            -f "--jscomp_error=unknownDefines"                                       \
            -f "--jscomp_error=visibility"                                           \
            -f "--js=assimilation/static/js/bin/deps.js"                                                 \
            -f "--create_source_map=assimilation/static/js/bin/$(1)-source-map"                          \
            -f "--variable_map_output_file=assimilation/static/js/bin/$(1)-var-map"                      \
            -f "--output_wrapper=\"(function() {%output%})();\""                     \
            --output_file=$(3);


#######################################
# JS (closure) Targets                #
#######################################

.PHONY: js clean-js
js: app gameclient
clean-js: clean-app clean-gameclient


.PHONY: deps clean-deps
deps: assimilation/static/js/bin/deps.js
clean-deps:
	rm -f assimilation/static/js/bin/deps.js

assimilation/static/js/bin/deps.js: $(COMPILED_JS_SOURCES)
	$(CALCDEPS)                                                           \
	-i assimilation/static/js/app/GameClient.js                           \
	-i assimilation/static/js/app/Client.js                               \
	-p assimilation/static/js/app                                         \
	-p assimilation/static/js/util                                        \
	-p assimilation/static/js/closure                                     \
	-o deps                                           \
	--output_file=$@

.PHONY: app clean-app
app: assimilation/static/js/bin/app.js
clean-app:
	rm -f assimilation/static/js/bin/app.js                               \
	      assimilation/static/js/bin/app-source-map                       \
	      assimilation/static/js/bin/app-var-map
assimilation/static/js/bin/app.js: assimilation/static/js/bin/deps.js
	$(call compilejs,app,assimilation/static/js/app/Client.js,$@)


.PHONY: gameclient clean-gameclient
gameclient: assimilation/static/js/bin/gameclient.js
clean-gameclient:
	rm -f assimilation/static/js/bin/gameclient.js
		  assimilation/static/js/bin/gameclient-source-map
		  assimilation/static/js/bin/gameclient-var-map
assimilation/static/js/bin/gameclient.js: assimilation/static/js/bin/deps.js
	$(call compilejs,gameclient,assimilation/static/js/app/GameClient.js,$@)



#######################################
# CSS Targets                         #
#######################################

.PHONY: css clean-css clean-css-compiled
css: $(LESS_CSS_COMPILED)
clean-css: clean-css-compiled
clean-css-compiled:
	rm -f $(LESS_CSS_COMPILED)

.SECONDARY: $(LESS_CSS_COMPILED)
assimilation/static/css/%.css: assimilation/static/css/%.less $(LESS_FILES)
	$(LESSC) $< -x > $@

#######################################
# CSS Targets                         #
#######################################
run:
	python manage.py runserver