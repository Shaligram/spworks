# .bashrc

# Source global definitions
if [ -f /etc/bashrc ]; then
	. /etc/bashrc
fi

# User specific aliases and functions
case "$TERM" in
    xterm-color) color_prompt=yes;;
esac
ncd=$HOSTNAME
alias ls='ls --color'
color_prompt=yes;
if [ "$color_prompt" = yes ]; then
#    PS1='${debian_chroot:+($debian_chroot)}\[\033[01;32m\]\u@\h\[\033[00m\]:\[\033[01;34m\]\[\033[00m\] '
    PS1='${debian_chroot:+($debian_chroot)}\[\033[01;32m\]\u@\h\[\033[00m\]:\[\033[01;34m\]`pwd`\[\033[00m\]\$ '
#    PS1='${debian_chroot:+($debian_chroot)}\[\033[01;32m\]\u\[\033[00m\]$ncd\[\033[01;34m\]\w\[\033[00m\]\$ '
#    PS1='${debian_chroot:+($debian_chroot)}\[\033[01;32m\]\u@\h\[\033[00m\]$\[\033[01;34m\]\w\033[00m\]\$ '
else
    PS1='${debian_chroot:+($debian_chroot)}\u@\h:\w\$ '
fi
source ~/.bash_aliases
alias ls='ls --color'
alias ll='ls -lrt --color'


