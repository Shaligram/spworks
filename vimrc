:set mouse=a
:set incsearch
:set syntax=on
:syn on
:set noic
:set nu
:set nowrap
:highlight Search ctermfg=white ctermbg=blue cterm=NONE
:set nows
:colorscheme elflord
:colorscheme murphy
:colorscheme ron


:set path+=**

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

" bind K to grep word under cursor
nnoremap K :silent :grep! "\b<C-R><C-W>\b"<CR>:cw<CR> :redraw! <CR>


" Silver Serachr Ends

set wildignore+=*/tmp/*,*/logs/,*/bin/*,*/bower_components/*,*/node_modules/*,*.so,*.swp,*.zip
set wildignore+=*/3rd-party/*,*/com/*,*.o,*.la,*.a,test.c,tags,*.log,
set wildignore+=*.o,*.obj,*~,*.pyc,.git/**,tags,cscope*

                                                                                                                                                                                             [68/407]
let g:ctrlp_working_path_mode = 0
:set tags+=./tags
:set tags+=/root/shaligram/vcm-gerrit-saegw/tags
:set tags+=/root/shaligram/vcm-gerrit-saegw/vcm-dpe/tags
:set tags+=/root/shaligram/vcm-gerrit-saegw/vcm-base/tags
:set tags+=/root/shaligram/vcm-gerrit-saegw/vcm-ms/tags
:set tags+=/root/shaligram/vcm-gerrit-saegw/vcm-cli/tags

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
:nmap '' :BufExplorer<CR>

map gn :bn<cr>
map gp :bp<cr>
map gd :bd<cr>

:set confirm

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
"autocmd FileType * call FoldPreprocessor()                                                                                                                                                  [22/407]
"function! FoldPreprocessor()
"    set foldmarker=ifdef,#endif
"    set foldmethod=marker
"endfunction


map l :foldclose<cr>

cnoremap <silent> q<CR>  :call ConfirmQuit(0)<CR>
cnoremap <silent> x<CR>  :call ConfirmQuit(1)<CR>
:set hls

set path=.,,**
set showcmd                                  " Showing what you are typing as command
set number                                   " Setting line numbers
set cursorline                               " Underlining the current line
set cursorcolumn                             " Highlight the current column
set hlsearch                                 " Highlight things that we find with the search

" open ctag in new tab
 map <C-\> :tab split<CR>:exec("tag ".expand("<cword>"))<CR>

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

" ack.vim Settings
 cnoreabbrev Ack Ack!
 " Shortcut for `:Ack! ` as `<Leader>a`
 nnoremap <Leader>a :Ack!<Space>
 let g:ackhighlight = 1                              " hightlight matches
if executable('ag')
 let g:ackprg = 'ag --nogroup -Q'    " Ag support
endif


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
":source /root/shaligram/.ackrc
:source /root/shaligram/ack.vim
nnoremap L :silent :Ack! "\b<C-R><C-W>\b" <CR>:cw<CR> :redraw! <CR>

