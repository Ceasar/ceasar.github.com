OBJS := $(addprefix posts/,joycons.html)

posts/joycons.html: posts/joycons.md
	pandoc $< -f markdown -t html > $@

all: $(OBJS)
	echo $(OBJS)
