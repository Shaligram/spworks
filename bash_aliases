#vncserver :64 -geometry 1920x1000  -depth 16
#vncserver :64 -geometry 1900x950 -depth 16
#vncserver :64 -geometry 1250x700 -depth 16
export NCP_TMP_DIR=/tmp/sprakash
alias tag='ctags --exclude="eth_oam" --exclude="gtpu"  --exclude="live_traffic_app" -R .'
alias lc='ls -ltr --color *.c *.h *.fpl *.fplh *.cnp'
alias lcs='ls -tr --color *.c *.h *.fpl *.fplh *.cnp'
alias lt='ls -lrt --color'
alias v6t='cd $ADK_SRC/ncp_adk/test/adk_samples/ipv6/'
alias aut='cd $ADK_SRC/ncp_adk/test/utils/test_auto/python/test_auto'
alias e6t='cd $ADK_SRC/ncp_adk/test/adk_samples/ethernet/'
alias v6c='cd $ADK_SRC/ncp_adk/code/adk_modules/ipv6/'
alias e6c='cd $ADK_SRC/ncp_adk/code/adk_modules/ethernet/'
alias v6m='cd $ADK_SRC/ncp_adk/test/adk_modules/ipv6/'
alias e6m='cd $ADK_SRC/ncp_adk/test/adk_modules/ethernet/'
alias v6f='cd $ADK_SRC/ncp_adk/code/config'
alias grepc='grep -nRTri --include=*.{c,fpl,fplh,h,cnp,tcl,exp,makefile} --color=always' 
#alias grep='grep -Ri --include=*.fpl'
alias c='clear'
alias v='view'
alias g='vi'
alias adk='cd $HOME/adk/'
alias adkr='cd $HOME/adk/rel_trunk_1'
alias wps='cd $ASE_REL'
alias 3448='source adk_linux-x86_3448.env'
alias 5516='source adk_linux-arma15_5516.env'
alias 5516h='echo "--------------------------------------------->Hardware Environment Sourced";source adk_linux-arma15_5516_hw.env'
export NCP_NCA_SOCKET=$HOSTNAME:99999
alias gd='$HOME/svndiff'
alias gv='$HOME/svndiff_vim'
alias ipcon=' sudo ifconfig eth4 192.168.56.155 netmask 255.255.255.0'
bind -x '"\C-e"':"make debug"
bind -x '"\C-f"':"make clean debug"
bind -x '"\C-g"':"make debug 2>&1 | tee buildlog.txt"
#bind -x '"\C-h"':"make clean debug 2>&1 | tee buildlog.txt"
alias shaldum='tcpdump -qns 0 -X -r' 
alias trk='cd $ADK_SRC;'
#export acpconf=../../../install/lib.linux-x86/adk_main_3448.cfg
alias acpdebug='acpdbg -E $NCP_TMP_DIR -H $ADK_SRC/ncp_adk/code/config/adk_main_5516.xml -t $ADK_SRC/ncp_adk/code/config/topology_5516.xml -c'
alias acpsimulator='acpsim -e $NCP_TMP_DIR -t $ADK_SRC/ncp_adk/code/config/topology_5516.xml -c'
#export DISPLAY=:64
export FPLC_GLOBAL_MULTI_THREAD=true
alias autorun='expect $ADK_SRC/ncp_adk/test/utils/test_auto/test_run'
alias rsyncm='rsync -arv --exclude=".*" --exclude="*.o" --exclude="*.d" --exclude="*.linux-arma15_exe" --exclude="*.doc" --exclude="*.docx" --exclude 'test''
#alias createconfig='../tools/createConfig.pl --config=adk_transportIP.ini'
alias baut='cd $ADK_SRC/ncp_adk/test/utils/dejagnu'
alias rebootboard='$ADK_ACP_TOOLS/axxReset.pl --host'
alias myshark='tshark -T fields -e eth -e vlan -r '
export SVN_EDITOR=vim
export ARMLMD_LICENSE_FILE=8225@fmylic7001.fm.intel.com


export http_proxy=http://proxy-chain.intel.com:911
#export https_proxy=http://proxy-chain.intel.com:912
#export ftp_proxy=http://proxy-chain.intel.com:911
#export socks_proxy=http://proxy-chain.intel.com:1080
#export no_proxy=intel.com,.intel.com,10.0.0.0/8,192.168.0.0/16,localhost,127.0.0.0/8,134.134.0.0/16

alias addjob='~/utility/addjob'
alias deljob='~/utility/deljob'
alias queryjob='~/utility/queryjob'
alias reserve='~/utility/reserve'

