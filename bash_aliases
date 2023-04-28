
# For UPF compilation
export SLOWPATH_DIR=/home/prakashsh/vcm-gerrit-upf
export MDP_PLAT_PATH=/home/prakashsh/mdp-vpp
# For UPF compilation Ends


stty erase ^?
#stty erase ^H·

if [[ $TMUX_PANE ]]; then
HISTFILE=/tmp/.bash_history_tmux_${TMUX_PANE:1}
fi


parse_git_branch() {
  git branch 2> /dev/null | sed -e '/^[^*]/d' -e 's/* \(.*\)/ (\1)/'
  }
export PS1="\u@\h \[\033[32m\]\w\[\033[33m\]\$(parse_git_branch)\[\033[00m\] $ "
export MYVIMRC=/home/shaligram/.vimrc

#vncserver :64 -geometry 1920x1000  -depth 16
#vncserver :64 -geometry 1900x950 -depth 16
#vncserver :64 -geometry 1250x700 -depth 16
#vncserver :64 -geometry 1580x780 -depth 16
export NCP_TMP_DIR=/tmp/sprakash
alias tag='ctags --exclude="eth_oam" --exclude="gtpu"  --exclude="live_traffic_app" -R .'
alias tag='ctags --exclude="*.o" --exclude="bin.debug" --exclude="vcm-install" -R .'
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
alias grepc='grep -nRTri --include=*.{c,cpp,h,hpp,tcl,xml} --color=always --include=Makefile --include=makefile'
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
alias gv='/home/prakashsh/shaligram/utility/svndiff'


#alias gv='echo -e "List of local files:\n" ;find . -type f | grep -v class$ | p4 -x - have > /dev/null; echo -e "\nList of to be added files: reconcile-n:";p4 reconcile -n ./... ; echo -e "\nList
#alias gv='~/utility/p4open_n_diff.sh $1'
#alias gvp='p4 changes -s pending ./...'


#alias gpp='p4 open $1 | sed -e 's/#.*//' | p4 -x - diff'
#  alias gp='$HOME/svndiff_vim'
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
  alias gitupsteam='git rev-parse --abbrev-ref --symbolic-full-name @{upstream}'
  alias gitco='git checkout'
  alias gitbr='git branch'
  alias deljob='~/utility/deljob'
  alias queryjob='~/utility/queryjob'
  alias reserve='~/utility/reserve'
  alias gvd='git difftool'
  alias gvds='git difftool --stat'
  alias gvds='gvds `git rev-parse --short HEAD~$1`'
#  alias gvs='git status . > /tmp/log ; grep -rw /tmp/log  -e "c" -e "tcl" -e "str" -e"pcap" -e"h" -e"fpl" -e"cnp" -e"fplh"'
  export TMPDIR=/tmp
#screen $SHELL -c 'screen -X caption always "ABC"'
  alias p4s='p4 changes -u sprakash -s shelved'
  export tb='/opt/opwv/integra/99.9/tools/vpp/'
  export PROMPT_COMMAND="echo -ne '\033k$YourVariable\033\\'"    # for setting the title in centos
  export SRC_BIN='mavenir@10.10.1.105:/home/mavenir/prakashsh/'
  alias p4local=' find ./ -type f | grep -v class$ | p4 -x - have > /dev/null;     '
  export PATH=$PATH:/opt/opwv/integra/SystemActivePath/tools/vpp/bin/:~/bin/
  sshcd () { ssh -t "$1" "cd \"$2\"; exec \$SHELL -l"; }

# Use vim to edit files
  export CSCOPE_EDITOR='vim'

# Generate cscope database
  function cscope_build() {
      # Generate a list of all source files starting from the current directory
      # The -o means logical or
      find . -name "*.c" -o -name "*.cc" -o -name "*.cpp" -o -name "*.h" -o -name "*.hh" -o -name "*.hpp" -name "*.xml" > cscope.files
          # -q build fast but larger database
          # -R search symbols recursively
          # -b build the database only, don't fire cscope
          # -i file that contains list of file paths to be processed
          # This will generate a few cscope.* files
          cscope -q -R -b -i cscope.files
            # Temporary files, remove them
            # rm -f cscope.files cscope.in.out cscope.po.out
            echo "The cscope database is generated for c++"
#!      ctags --exclude="*.o" --exclude="bin.debug" --exclude="vcm-install" --exclude=".json" --exclude="*.xml" -R .
        ctags --exclude="*.o" --exclude="bin.debug" --exclude="vcm-install" --exclude="*schema*" --exclude="*.xml" --exclude="*.js" --exclude="*.tpl" --exclude="*.yaml" --exclude="*Makefile*" --exclude="*tests*" -R .
!·!·  echo "Ctags generated"
  }
# -d don't build database, use kscope_generate explicitly
#alias cscope=cscope -d'
unset PROMPT_COMMAND
alias vim='vim -S /home/prakashsh/shaligram/.vimrc'
alias vi='vim -S /home/prakashsh/shaligram/.vimrc'
alias vimdiff='vimdiff -S /home/prakashsh/shaligram/.vimrc'
export VIMINIT='source /home/prakashsh/shaligram/.vimrc'
export ACKRC="/home/prakashsh/shaligram/.ackrc"
alias doc=" docker run -u root:root -v /local:/local -w /local/ -v /home/prakashsh:/home/prakashsh -w /home/prakashsh/ --name SP-UPF-FRR --rm -it xxx.com/platform/buildcentos7:1.30_4.8"

~

