Present=1
HostName=10.20.31.59
LogFileName=putty.log
LogType=0
LogFileClash=-1
LogFlush=1
SSHLogOmitPasswords=1
SSHLogOmitData=0
Protocol=ssh
PortNumber=22
CloseOnExit=1
WarnOnClose=1
PingInterval=0
PingIntervalSecs=0
TCPNoDelay=1
TCPKeepalives=0
TerminalType=xterm
TerminalSpeed=38400,38400
TerminalModes=CS7=A,CS8=A,DISCARD=A,DSUSP=A,ECHO=A,ECHOCTL=A,ECHOE=A,ECHOK=A,ECHOKE=A,ECHONL=A,EOF=A,EOL=A,EOL2=A,ERASE=A,FLUSH=A,ICANON=A,ICRNL=A,IEXTEN=A,IGNCR=A,IGNPAR=A,IMAXBEL=A,INLCR=A,INPCK=A,INTR=A,ISIG=A,ISTRIP=A,IUCLC=A,IUTF8=A,IXANY=A,IXOFF=A,IXON=A,KILL=A,LNEXT=A,NOFLSH=A,OCRNL=A,OLCUC=A,ONLCR=A,ONLRET=A,ONOCR=A,OPOST=A,PARENB=A,PARMRK=A,PARODD=A,PENDIN=A,QUIT=A,REPRINT=A,START=A,STATUS=A,STOP=A,SUSP=A,SWTCH=A,TOSTOP=A,WERASE=A,XCASE=A
AddressFamily=0
ProxyExcludeList=
ProxyDNS=1
ProxyLocalhost=0
ProxyMethod=0
ProxyHost=proxy
ProxyPort=80
ProxyUsername=
ProxyPassword=
ProxyTelnetCommand=connect %host %port\n
Environment=
UserName=
UserNameFromEnvironment=0
LocalUserName=
NoPTY=0
Compression=0
TryAgent=1
AgentFwd=0
GssapiFwd=0
ChangeUsername=0
Cipher=aes,chacha20,blowfish,3des,WARN,arcfour,des
KEX=ecdh,dh-gex-sha1,dh-group14-sha1,rsa,WARN,dh-group1-sha1
RekeyTime=60
RekeyBytes=1G
SshNoAuth=0
SshBanner=1
AuthTIS=0
AuthKI=1
AuthGSSAPI=1
GSSLibs=gssapi32,sspi,custom
GSSCustom=
SshNoShell=0
SshProt=3
LogHost=
SSH2DES=0
PublicKeyFile=
RemoteCommand=
RFCEnviron=0
PassiveTelnet=0
BackspaceIsDelete=1
RXVTHomeEnd=0
LinuxFunctionKeys=0
NoApplicationKeys=0
NoApplicationCursors=0
NoMouseReporting=0
NoRemoteResize=0
NoAltScreen=0
NoRemoteWinTitle=0
RemoteQTitleAction=1
NoDBackspace=0
NoRemoteCharset=0
ApplicationCursorKeys=0
ApplicationKeypad=0
NetHackKeypad=0
AltF4=1
AltSpace=0
AltOnly=0
ComposeKey=0
CtrlAltKeys=1
TelnetKey=0
TelnetRet=1
LocalEcho=2
LocalEdit=2
Answerback=PuTTY
AlwaysOnTop=0
FullScreenOnAltEnter=0
HideMousePtr=0
SunkenEdge=0
WindowBorder=1
CurType=0
BlinkCur=1
Beep=1
BeepInd=0
BellWaveFile=
BellOverload=1
BellOverloadN=5
BellOverloadT=2000
BellOverloadS=5000
ScrollbackLines=20000
DECOriginMode=0
AutoWrapMode=1
LFImpliesCR=0
CRImpliesLF=0
DisableArabicShaping=0
DisableBidi=0
WinNameAlways=1
WinTitle=bfs-dl360g7-73.bfs.openwave.com - PuTTY
TermWidth=80
TermHeight=24
FontName=Courier New
Font=Courier New
FontIsBold=0
FontCharSet=0
FontHeight=10
FontQuality=0
FontVTMode=4
UseSystemColours=0
TryPalette=0
ANSIColour=1
Xterm256Colour=1
BoldAsColour=1
Colour0=187,187,187
Colour1=255,255,255
Colour2=0,0,0
Colour3=85,85,85
Colour4=0,0,0
Colour5=0,255,0
Colour6=0,0,0
Colour7=85,85,85
Colour8=187,0,0
Colour9=255,85,85
Colour10=0,187,0
Colour11=85,255,85
Colour12=187,187,0
Colour13=255,255,85
Colour14=0,0,187
Colour15=85,85,255
Colour16=187,0,187
Colour17=255,85,255
Colour18=0,187,187
Colour19=85,255,255
Colour20=187,187,187
Colour21=255,255,255
RawCNP=0
PasteRTF=0
MouseIsXterm=0
RectSelect=0
MouseOverride=1
Wordness0=0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
Wordness32=0,1,2,1,1,1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,2,2,2,2,1,1,1,1,1,1
Wordness64=1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1,1,1,1,2
Wordness96=1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1,1,1,1,1
Wordness128=1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1
Wordness160=1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1
Wordness192=2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1,2,2,2,2,2,2,2,2
Wordness224=2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1,2,2,2,2,2,2,2,2
LineCodePage=
CJKAmbigWide=0
UTF8Override=1
Printer=
CapsLockCyr=0
ScrollBar=1
ScrollBarFullScreen=0
ScrollOnKey=0
ScrollOnDisp=1
EraseToScrollback=1
LockSize=0
BCE=1
BlinkText=0
X11Forward=0
X11Display=
X11AuthType=1
X11AuthFile=
LocalPortAcceptAll=0
RemotePortAcceptAll=0
PortForwardings=
BugIgnore1=0
BugPlainPW1=0
BugRSA1=0
BugIgnore2=0
BugHMAC2=0
BugDeriveKey2=0
BugRSAPad2=0
BugPKSessID2=0
BugRekey2=0
BugMaxPkt2=0
BugOldGex2=0
BugWinadj=0
BugChanReq=0
StampUtmp=1
LoginShell=1
ScrollbarOnLeft=0
BoldFontName=
BoldFont=
BoldFontIsBold=0
BoldFontCharSet=0
BoldFontHeight=0
WideFontName=
WideFont=
WideFontIsBold=0
WideFontCharSet=0
WideFontHeight=0
WideBoldFontName=
WideBoldFont=
WideBoldFontIsBold=0
WideBoldFontCharSet=0
WideBoldFontHeight=0
ShadowBold=0
ShadowBoldOffset=1
SerialLine=COM1
SerialSpeed=9600
SerialDataBits=8
SerialStopHalfbits=2
SerialParity=0
SerialFlowControl=1
WindowClass=
ConnectionSharing=0
ConnectionSharingUpstream=1
ConnectionSharingDownstream=1
SSHManualHostKeys=
NoRemoteTabName=0
NoRemoteTabNameInIcon=1
LinesAtAScroll=3
AutocmdEnable0=1
AutocmdExpect0=ogin: 
Autocmd0=
AutocmdEncrypted0=0
AutocmdHide0=0
AutocmdEnable1=1
AutocmdExpect1=assword: 
Autocmd1=
AutocmdEncrypted1=0
AutocmdHide1=1
AutocmdCount=2
AdbConStr=
AdbCmdStr=&padb.exe -s &1 shell
AdbDevScanInterval=0
AdbCompelCRLF=1
DataVersion=2
GroupCollapse=1