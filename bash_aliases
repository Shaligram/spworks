#/nfs-bfs/local/cppcheck/cppcheck-2.3/cppcheck --enable=warning,performance  --platform=native --language=c++ --std=c++03 -I $DERBASE/include --inline-suppr .
#
export P4PORT=bfs-p4.bfs.openwave.com:1667
#export P4PORT=bfs-p4.bfs.openwave.com:7592
export P4CONFIG=p4.config
export P4EDITOR=vim
export P4USER=sprakash
#export P4CLIENT=sprakash.integra.6.3.2.X
export P4CLIENT=sprakash.integra.7.1
export P4DIFF=vimdiff
export P4IGNORE=$HOME/.p4ignore

shopt -s direxpand
export CSCOPE_EDITOR=vim
unset PROMPT_COMMAND

#vncserver :64 -geometry 1920x1000  -depth 16
#vncserver :64 -geometry 1900x950 -depth 16
#vncserver :64 -geometry 1250x700 -depth 16
#vncserver :64 -geometry 1580x780 -depth 16
export NCP_TMP_DIR=/tmp/sprakash
alias tag='ctags --exclude="eth_oam" --exclude="gtpu"  --exclude="live_traffic_app" -R .'
alias lc='ls -ltrh --color *.c *.h *.fpl *.fplh *.cnp'
alias lcs='ls -trh --color *.c *.h *.fpl *.fplh *.cnp'
alias lt='ls -lrth --color'
alias v6t='cd $ADK_SRC/ncp_adk/test/adk_samples/ipv6/'
alias aut='cd ${ADK_SRC}_test/utils/test_auto/python/test_auto'
alias e6t='cd ${ADK_SRC}/ncp_adk/test/adk_samples/ethernet/'
alias v6c='cd $ADK_SRC/ncp_adk/code/adk_modules/ipv6/'
alias e6c='cd $ADK_SRC/ncp_adk/code/adk_modules/ethernet/'
alias v6m='cd ${ADK_SRC}_test/adk_modules/ipv6/'
alias e6m='cd ${ADK_SRC}_test/adk_modules/ethernet/'
alias v6f='cd $ADK_SRC/ncp_adk/code/config'
alias grepc='grep -nRTri --include=*.{c,fpl,fplh,h,cnp,tcl,exp} --color=always --include=Makefile --include=makefile' 
#alias grep='grep -Ri --include=*.fpl'
alias c='clear'
alias v='vim +TlistOpen'
#alias vi='vim -p '
alias adk='cd $SRC_HEAD'
alias wps='cd $ASE_REL'
alias setp4env='source .environ; echo $P4CLIENT; echo $SYS_BASE'
alias 5516='source adk_linux-arma15_5516.env'
alias 5516h='echo "--------------------------------------------->Hardware Environment Sourced";source adk_linux-arma15_5516_hw.env'
export NCP_NCA_SOCKET=$HOSTNAME:99999
alias gd='$HOME/svndiff'


#alias gv='echo -e "List of local files:\n" ;find . -type f | grep -v class$ | p4 -x - have > /dev/null; echo -e "\nList of to be added files: reconcile-n:";p4 reconcile -n ./... ; echo -e "\nList of modified files:\n";p4 diff -f -sa ./...'
alias gv='~/utility/p4open_n_diff.sh $1'
alias gvp='p4 changes -s pending ./...'




#alias gpp='p4 open $1 | sed -e 's/#.*//' | p4 -x - diff'
alias gp='$HOME/svndiff_vim'
alias ipcon=' sudo ifconfig eth4 192.168.56.155 netmask 255.255.255.0'
#bind -x '"\C-e"':"make build"
#bind -x '"\C-f"':"make clean debug"
#bind -x '"\C-g"':"make debug 2>&1 | tee buildlog.txt"
#bind -x '"\C-h"':"make clean debug 2>&1 | tee buildlog.txt"
alias shaldum='tcpdump -qns 0 -X -r' 
alias trk='cd $SRC_HEAD;'
alias trkk='cd /users/sprakash/mainline/experimental/vpp/plugins/opwv_tcpproxy'
#export acpconf=../../../install/lib.linux-x86/adk_main_3448.cfg
alias acpdebug='acpdbg -E $NCP_TMP_DIR -H $ADK_SRC/ncp_adk/code/config/adk_main_6732.xml -t $ADK_SRC/ncp_adk/code/config/topology_6732.xml -c'
alias acpsimulator='acpsim -e $NCP_TMP_DIR -t $ADK_SRC/ncp_adk/code/config/topology_5516.xml -c'
export FPLC_GLOBAL_MULTI_THREAD=true
alias autorun='expect $ADK_SRC/ncp_adk/test/utils/test_auto/test_run'
alias rsyncm='rsync -arv --exclude=".*" --exclude="*.o" --exclude="*.d" --exclude="*.linux-arma15_exe" --exclude="*.doc" --exclude="*.docx" --exclude 'test''
alias createconfig='../tools/createConfig.pl --config=adk_transportIP.ini'
alias baut='cd ${ADK_SRC}_test/utils/dejagnu'
alias rebootboard='$ADK_ACP_TOOLS/axxReset.pl --host'
alias myshark='tshark -T fields -e eth -e vlan -r '
export SVN_EDITOR=vim


alias gitlog=" git log --graph --pretty=format:'%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset' --abbrev-commit --max-count"
alias githead='git log --pretty=format:"%Cred%h%Creset-%C(bold blue)%d%Creset %Cgreen%ar%Creset:%Cred%an%Creset, %s" --max-count'
alias deljob='~/utility/deljob'
alias queryjob='~/utility/queryjob'
alias reserve='~/utility/reserve'
alias gvd='git difftool'
alias gvs='git status . > /tmp/log ; grep -rw /tmp/log  -e "c" -e "tcl" -e "str" -e"pcap" -e"h" -e"fpl" -e"cnp" -e"fplh"'
export TMPDIR=/tmp
#screen $SHELL -c 'screen -X caption always "ABC"'
alias p4s='p4 changes -u sprakash -s shelved'
export tb='/opt/opwv/integra/99.9/tools/vpp/'
export PROMPT_COMMAND="echo -ne '\033k$YourVariable\033\\'"    # for setting the title in centos
alias p4local=' find ./ -type f | grep -v class$ | p4 -x - have > /dev/null;     '
export PATH=$PATH:/opt/opwv/integra/SystemActivePath/tools/vpp/bin/
sshcd () { ssh -t "$1" "cd \"$2\"; exec \$SHELL -l"; }

alias p4diff="p4 changes -l \"...#>have\""
#stty cols 132 rows 200 -> set the rows in terminal of screen to higher value
