OBJS := $(addprefix posts/,joycons.html memex_meetup_2.html)

posts/%.html: posts/%.md
	pandoc $< -f markdown -t html > $@

all: $(OBJS)
