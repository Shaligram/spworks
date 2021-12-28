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
                                                                                                                                                                                            [39/9390]
":command! -nargs=+ Mmsearch vimgrep /<args>/gj /<args>/**/*.c **/*.h **/*.cpp **/*.hpp **/*.xml |cw
:command! -nargs=+ Mmsearch vimgrep /<args>/gj <args>/**/* |cw

" The Silver Searcher
if executable('ag')
" Use ag over grep
"set grepprg=ag\ --silent\ --nocolor
set grepprg=ag\ --vimgrep\ $*
" Use ag in CtrlP for listing files. Lightning fast and respects .gitignore
let g:ctrlp_user_command = 'ag %s -l -g ""'
"ag is fast enough that CtrlP doesn't need to cache
let g:ctrlp_use_caching = 1
endif
" bind K to grep word under cursor
 nnoremap K :silent :grep! "\b<C-R><C-W>\b"<CR>:cw<CR> :redraw! <CR>

"Search Visual Text by \\
vnoremap // y/\V<C-R>=escape(@",'/\')<CR><CR>


command! -nargs=1 Search call MySearch(<q-args>)
function! MySearch(grep_term)
" upper logic
   execute 'silent grep' a:grep_term | copen
"   " lower logic
   endfunction

" Silver Serachr

:set wildignore+=bin/**,3rd-party/**,com/**,*.o,*.la,*.a,test.c



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
:nmap <F3> :vimgrep<space>  %|cw

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

cnoremap <silent> q<CR>  :call ConfirmQuit(0)<CR>
cnoremap <silent> x<CR>  :call ConfirmQuit(1)<CR>
:set hls
