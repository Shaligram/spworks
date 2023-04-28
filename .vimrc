set mouse=a
set incsearch
set syntax=on
:syn on
set noic
set nu
set nowrap
:highlight Search ctermfg=white ctermbg=blue cterm=NONE
set nows
:colorscheme elflord
:colorscheme murphy
:colorscheme desert
:colorscheme ron

filetype indent on
set smartindent
autocmd BufRead,BufWritePre *.sh normal gg=G

set backspace=indent,eol,start

"set guitablabel=\[%N\]\ %t\ %M 

set path+=**

":command! -nargs=+ Mmsearch vimgrep /<args>/gj /<args>/**/*.c **/*.h **/*.cpp **/*.hpp **/*.xml |cw
:command! -nargs=+ Mmsearch vimgrep /<args>/gj <args>/**/* |cw


" The Silver Searcher
if executable('ag')
" Use ag over grep
" set grepformat=%f:%l:%c:%m
 set grepprg=ag\ --nogroup\ --nocolor
"set grepprg=ag\ --vimgrep\ $*
" Use ag in CtrlP for listing files. Lightning fast and respects .gitignore
let g:ctrlp_user_command = 'ag %s -l -g ""'
"ag is fast enough that CtrlP doesn't need to cache
let g:ctrlp_use_caching = 1
endif
" Silver Serachr Ends
let g:ctrlp_working_path_mode = 0

set wildignore+=*/tmp/*,*/logs/,*/bin/*,*/bower_components/*,*/node_modules/*,*.so,*.swp,*.zip
"set wildignore+=*/3rd-party/*,*/com/*,*.o,*.la,*.a,test.c,*.log,
"set wildignore+=*.o,*.obj,*~,*.pyc,.git/*,

"Tag list per dire
let cwd = getcwd()

if (match(cwd, "/home/prakashsh/vcm-gerrit-saegw/") == 0)
    set tags=/home/prakashsh//vcm-gerrit-saegw/tags;
    set tags+=/home/prakashsh//vcm-gerrit-saegw/vcm-dpe/tags;
    set tags+=/home/prakashsh//vcm-gerrit-saegw/vcm-base/tags;
    set tags+=/home/prakashsh//vcm-gerrit-saegw/vcm-ms/tags;
    set tags+=/home/prakashsh//vcm-gerrit-saegw/vcm-cli/tags;
elseif (match(cwd, "/home/prakashsh/vcm-gerrit-upf/") == 0)
    set tags=/home/prakashsh//vcm-gerrit-upf/tags;
    set tags+=/home/prakashsh//vcm-gerrit-upf/vcm-dpe/tags;
    set tags+=/home/prakashsh//vcm-gerrit-upf/vcm-base/tags;
    set tags+=/home/prakashsh//vcm-gerrit-upf/vcm-ms/tags;
    set tags+=/home/prakashsh//vcm-gerrit-upf/vcm-cli/tags;
else
    set tags=/home/prakashsh//581-vcm-gerrit-saegw/tags;
endif

" Reopen the last edited position in files
au BufReadPost * if line("'\"") > 1 && line("'\"") <= line("$") | exe "normal! g'\"" | endif


fun! ShowFuncName()
    let lnum = line(".")
    let col = col(".")
    echohl ModeMsg
    echo getline(search("^[^ \t#/]\\{2}.*[^:]\s*$", 'bW'))
    echohl None
    call search("\\%" . lnum . "l" . "\\%" . col . "c")
endfun
map f :call ShowFuncName() <CR>

:highlight Search ctermfg=white ctermbg=blue cterm=NONE
set confirm

function! ConfirmQuit(writeFile)
  if (a:writeFile)
    if (expand('%:t')=="")
      echo "Can't save a file with no name."
      return
    endif
    :write
  endif
  if (winnr('$')==1 && tabpagenr('$')==1)
    if (confirm("Do you really want to quit?", "&Yes\n&No", 2)==1)
      :quit
    endif
  else
    :quit
  endif
endfu


"autocmd FileType * call FoldPreprocessor()
"function! FoldPreprocessor()
"    set foldmarker=ifdef,#endif
"    set foldmethod=marker
"endfunction



set hls

set path=.,,** 
set showcmd                                  " Showing what you are typing as command
"set cursorline                               " Underlining the current line
"set cursorcolumn                             " Highlight the current column
set hlsearch                                 " Highlight things that we find with the search
set cursorbind

" list all mapping using `:map`
" " if you do `Ctrol-k` and then press a key, the vim
" " will tell you how this key is know to vim


" CtrlP Settings
 set runtimepath^=~/.vim/bundle/ctrlp.vim     " enabling Fuzzy Search
 let g:ctrlp_max_files=0                      " number of files to scan initially
 let g:ctrlp_max_depth=25                     " directory depth to recurse into when scanning
 " for CtrlP in MacOSX/Linux
 let g:ctrlp_custom_ignore = {
 \ 'dir':  '\v[\/]\.(git|hg|svn)$',
 \ 'file': '\v\.(exe|so|dll)$',
 \ 'link': 'some_bad_symbolic_links',
 \ }
" let g:ctrlp_user_command = ['.git', 'cd %s && git ls-files -co --exclude-standard']      " Ignore files in .gitignore (does not given right results)

" open ctag in new tab
map <C-\> :tab split<CR>:exec("tag ".expand("<cword>"))<CR>
map '' :BufExplorer<CR>
map qd :bd <CR>
map qq :qa! <CR>
map ww :w!<cr>
map gd :bd<cr>  
map l :foldclose<cr>  

" ack.vim Settings
cnoreabbrev Ack Ack!
 " Shortcut for `:Ack! ` as `<Leader>a`
nnoremap <Leader>a :Ack!<Space>
"export the ACKRC in bash aliases
nnoremap L :silent :Ack! "\b<C-R><C-W>\b" <CR>:cw<CR> :redraw! <CR>
" bind K to grep word under cursor
nnoremap K :silent :grep! "\b<C-R><C-W>\b"<CR>:cw<CR> :redraw! <CR>
cnoremap <silent> q<CR>  :call ConfirmQuit(0)<CR>
cnoremap <silent> qa<CR>  :call ConfirmQuit(0)<CR>
cnoremap <silent> x<CR>  :call ConfirmQuit(1)<CR>
 let g:ackhighlight = 1                              " hightlight matches
"if executable('ag')
" let g:ackprg = 'ag --nogroup '    " Ag support
"endif


" vim-markdown Settings
let g:vim_markdown_folding_disabled = 1               " disable folding in vim-markdown
let g:vim_markdown_toc_autofit = 1                    " autofix TOC
let g:vim_markdown_follow_anchor = 1                  " follow markdown links with `ge` command
let g:vim_markdown_anchorexpr = "'<<'.v:anchor.'>>'"
let g:vim_markdown_edit_url_in = 'tab'                " open links in new tab instead of in current buffer
let g:vim_markdown_conceal = 0                        " disable conceal for markdown
let g:vim_markdown_conceal_code_blocks = 0            " don't conceal code blocks

set autoindent
"show hide special syms
set nolist

"Delete all trailing whitespaces
"%s/\s\+$//
"
set shiftwidth=4


"Disabled cstag instead of vim tag
"set nocst
":set tags?  > query the files


" Some funky status bar code its seems
" https://stackoverflow.com/questions/9065941/how-can-i-change-vim-status-line-colour
set laststatus=2            " set the bottom status bar
function! ModifiedColor()
    if &mod == 1
        hi statusline guibg=White ctermfg=8 guifg=OrangeRed4 ctermbg=6
    else
        hi statusline guibg=White ctermfg=8 guifg=DarkSlateGray ctermbg=2
    endif
endfunction

"au InsertLeave,InsertEnter,BufWritePost   * call ModifiedColor()
" default the statusline when entering Vim
hi statusline guibg=White ctermfg=4 guifg=DarkSlateGray ctermbg=7

" Formats the statusline
set statusline=[%n]\ \                     " Buffer number
set statusline+=[%f]\ \                          " file name
set statusline+=[%{getbufvar(bufnr('%'),'&mod')?'modified':'saved'}]     "modified flag
"set statusline+=[%{strlen(&fenc)?&fenc:'none'}, "file encoding
"set statusline+=[%{&ff}] "file format
set statusline+=[%y]      "filetype
set statusline+=%h      "help file flag
set statusline+=%r      "read only flag
"set statusline+=\ %=                        " align left
set statusline+=[LINE:%l/%L][%p%%]            " line X of Y [percent of file]
set statusline+=\ Col:%c                    " current column
set statusline+=\ [%b][0x%B]\               " ASCII and byte code under cursorY

"curl https://beyondgrep.com/ack-v3.5.0 > ~/bin/ack && chmod 0755 ~/bin/ack
:source /home/prakashsh/shaligram/ack.vim
:source /home/prakashsh/shaligram/taglist.vim
:source /home/prakashsh/shaligram/bufexplorer.vim


set tabstop=2 shiftwidth=4 expandtab
set list
set listchars=tab:!·,trail:·
"set listchars=tab:!·,
"
