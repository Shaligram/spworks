filetype plugin indent on

:set ls=4
:set incsearch
:set syntax=on
:set guifont=Monospace\ Regular\ 9
:set ic
:set nu
:set hls!
:syn on 
:colorscheme evening
:set syntax=c
au BufReadPost *.fpl set syntax=c 
"nmap <F3> :redir @a<CR>:silent g//<CR>j<CR>:redir END<CR>:new<CR>:put!a<CR><CR>
"nmap <F3> :redir @a<CR>:silent g//<CR>j<CR>:redir END<CR>:new<CR>:put!a<CR><CR>
:nmap  :%s/
//g
:set nowrap
:highlight Search ctermfg=white ctermbg=blue cterm=NONE
":highlight OverLength ctermbg=cyan ctermfg=white guibg=#592929
":match OverLength /\%89v.\+/
:nmap <F9> :tabnext<CR>
:nmap <F8> :tabprevious<CR>
:nmap <F10> :e!<CR>
" If the current buffer has never been saved, it will have no name,
" " call the file browser to save it, otherwise just save it.
"nnoremap <silent> <C-S> :if expand("%") == ""<CR>browse confirm w<CR>else<CR>confirm w<CR>endif<CR>
:set nows

" Uncomment the following to have Vim jump to the last position when                                                       
" reopening a file
if has("autocmd")
  au BufReadPost * if line("'\"") > 0 && line("'\"") <= line("$")
    \| exe "normal! g'\"" | endif
endif
:set mouse=a

:set expandtab
:set shiftwidth=4
:set softtabstop=4
"below changes width to wrap test in a single line
:set textwidth=160
:set nonu
:set cindent

:set tags=$ADK_SRC/tags
:set tags=tags

"nnoremap <C-p> :!/usr/bin/firefox %<CR>

:set nu

" check file change every 4 seconds ('CursorHold') and reload the buffer upon detecting change
":set autoread                                                                                                                                                                                    
"au CursorHold * 4 

fun! ShowFuncName()
 let lnum = line(".")
 let col = col(".")
 echohl ModeMsg
 echo getline(search("^[^ \t#/]\\{2}.*[^:]\s*$", 'bW'))
 echohl None
 call search("\\%" . lnum . "l" . "\\%" . col . "c")
endfun
map f :call ShowFuncName() <CR>

" Status Line {  
        set laststatus=2                             " always show statusbar  
        set statusline=  
        set statusline+=%-10.3n\                     " buffer number  
        set statusline+=%f\                          " filename   
        set statusline+=%h%m%r%w                     " status flags  
        "       set statusline+=\[%{strlen(&ft)?&ft:'none'}] " file type  
        "set statusline+=%=                           " right align remainder  
        " set statusline+=0x%-8B                       " character value  
        set statusline+=%-14(%l,%c%V%)               " line, character  
        set statusline+=%<%P                         " file position  
"}  

