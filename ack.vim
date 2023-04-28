let s:last_search_args = []

if !exists("g:ack_default_options")
  let g:ack_default_options = " -s -H --nocolor --nogroup --column"
endif

" Location of the ack utility
if !exists("g:ackprg")
  if executable('ack')
    let g:ackprg = "ack"
  elseif executable('ack-grep')
    let g:ackprg = "ack-grep"
  else
    finish
  endif
  let g:ackprg .= g:ack_default_options
endif

if !exists("g:ack_apply_qmappings")
  let g:ack_apply_qmappings = !exists("g:ack_qhandler")
endif

if !exists("g:ack_apply_lmappings")
  let g:ack_apply_lmappings = !exists("g:ack_lhandler")
endif

if !exists("g:ack_use_dispatch")
  let g:ack_use_dispatch = 0
end

let s:ack_mappings = {
      \ "t": "<C-W><CR><C-W>T",
      \ "T": "<C-W><CR><C-W>TgT<C-W>j",
      \ "o": "<CR>",
      \ "O": "<CR><C-W>p<C-W>c",
      \ "go": "<CR><C-W>p",
      \ "h": "<C-W><CR><C-W>K",
      \ "H": "<C-W><CR><C-W>K<C-W>b",
      \ "v": "<C-W><CR><C-W>H<C-W>b<C-W>J<C-W>t",
      \ "gv": "<C-W><CR><C-W>H<C-W>b<C-W>J" }

if exists("g:ack_mappings")
  let g:ack_mappings = extend(s:ack_mappings, g:ack_mappings)
else
  let g:ack_mappings = s:ack_mappings
endif

if !exists("g:ack_qhandler")
  let g:ack_qhandler = "botright copen"
endif

if !exists("g:ack_lhandler")
  let g:ack_lhandler = "botright lopen"
endif

if !exists("g:ackhighlight")
  let g:ackhighlight = 0
endif

if !exists("g:ack_autoclose")
  let g:ack_autoclose = 0
endif

if !exists("g:ack_autofold_results")
  let g:ack_autofold_results = 0
endif

function! s:Ack(cmd, args, count)
  let s:last_search_args = [a:cmd, a:args, a:count]

  redraw
  echo "Searching ..."

  if a:count > 0
    " then we've selected something in visual mode
    let l:grepargs = shellescape(fnameescape(s:LastSelectedText()))
  elseif empty(a:args)
    " If no pattern is provided, search for the word under the cursor
    let l:grepargs = expand("<cword>")
  else
    let l:grepargs = a:args . join(a:000, ' ')
  end

  " Format, used to manage column jump
  if a:cmd =~# '-g$'
    let g:ackformat="%f"
  else
    let g:ackformat="%f:%l:%c:%m"
  end

  let grepprg_bak=&grepprg
  let grepformat_bak=&grepformat
  try
    let &grepprg=g:ackprg
    let &grepformat=g:ackformat
    silent execute a:cmd . " " . escape(l:grepargs, '|')
  finally
    let &grepprg=grepprg_bak
    let &grepformat=grepformat_bak
  endtry

  if a:cmd =~# '^l'
    exe g:ack_lhandler
    let l:apply_mappings = g:ack_apply_lmappings
  else
    exe g:ack_qhandler
    let l:apply_mappings = g:ack_apply_qmappings
  endif

  if l:apply_mappings
    exec "nnoremap <silent> <buffer> q :ccl<CR>"
    exec "nnoremap <silent> <buffer> t <C-W><CR><C-W>T"
    exec "nnoremap <silent> <buffer> T <C-W><CR><C-W>TgT<C-W><C-W>"
    exec "nnoremap <silent> <buffer> o <CR>"
    exec "nnoremap <silent> <buffer> go <CR><C-W><C-W>"
    exec "nnoremap <silent> <buffer> h <C-W><CR><C-W>K"
    exec "nnoremap <silent> <buffer> H <C-W><CR><C-W>K<C-W>b"
    exec "nnoremap <silent> <buffer> v <C-W><CR><C-W>H<C-W>b<C-W>J<C-W>t"
    exec "nnoremap <silent> <buffer> gv <C-W><CR><C-W>H<C-W>b<C-W>J"
  endif

  " If highlighting is on, highlight the search keyword.
  if exists("g:ackhighlight")
    let @/=a:args
    set hlsearch
  end

  redraw!
endfunction

function! s:AckRerun()
  if empty(s:last_search_args)
    echoerr "There's no previous search to rerun"
    return
  endif

  call call('s:Ack', s:last_search_args)
endfunction

function! s:AckFromSearch(cmd, args)
  let search =  getreg('/')
  " translate vim regular expression to perl regular expression.
  let search = substitute(search,'\(\\<\|\\>\)','\\b','g')
  call s:Ack(a:cmd, '"' .  search .'" '. a:args)
endfunction

function! s:GetDocLocations()
  let dp = ''
  for p in split(&rtp,',')
    let p = p.'/doc/'
    if isdirectory(p)
      let dp = p.'*.txt '.dp
    endif
  endfor
  return dp
endfunction

function! s:AckHelp(cmd,args)
  let args = a:args.' '.s:GetDocLocations()
  call s:Ack(a:cmd,args)
endfunction

function! s:AckOption(bang, ...)
  for option in a:000
    let remove      = (a:bang == '!')
    let base_option = substitute(option, '^no', '', '')
    let pattern     = '\v\s+--(no)?\V'.base_option

    if remove
      let replacement = ''
    else
      let replacement = ' --'.option
    endif

    if g:ackprg =~ pattern
      let g:ackprg = substitute(g:ackprg, pattern, replacement, '')
    else
      let g:ackprg .= ' --'.option
    endif
  endfor

  echo 'Ack called as: '.g:ackprg
endfunction

function! s:AckIgnore(bang, ...)
  for directory in a:000
    silent call s:AckOption(a:bang, 'ignore-dir="' . directory . '"')
  endfor

  echo 'Ack called as: '.g:ackprg
endfunction

function! s:LastSelectedText()
  let saved_cursor = getpos('.')

  let original_reg      = getreg('z')
  let original_reg_type = getregtype('z')

  normal! gv"zy
  let text = @z

  call setreg('z', original_reg, original_reg_type)
  call setpos('.', saved_cursor)

  return text
endfunction

command! -bang -nargs=* -complete=file -range=0 Ack call s:Ack('grep<bang>',<q-args>, <count>)

command! AckRerun call s:AckRerun()

command! -bang -nargs=* -complete=file AckAdd        call s:Ack('grepadd<bang>', <q-args>, 0)
command! -bang -nargs=* -complete=file AckFromSearch call s:AckFromSearch('grep<bang>', <q-args>)
command! -bang -nargs=* -complete=file LAck          call s:Ack('lgrep<bang>', <q-args>, 0)
command! -bang -nargs=* -complete=file LAckAdd       call s:Ack('lgrepadd<bang>', <q-args>, 0)
command! -bang -nargs=* -complete=file AckFile       call s:Ack('grep<bang> -g', <q-args>, 0)
command! -bang -nargs=* -complete=help AckHelp       call s:AckHelp('grep<bang>',<q-args>)
command! -bang -nargs=* -complete=help LAckHelp      call s:AckHelp('lgrep<bang>',<q-args>)

command! -bang -nargs=*                AckOption call s:AckOption('<bang>', <f-args>)
command! -bang -nargs=* -complete=file AckIgnore call s:AckIgnore('<bang>', <f-args>)
