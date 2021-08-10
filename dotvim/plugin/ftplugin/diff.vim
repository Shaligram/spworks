
" Go to diff for files from diff for dirs output
" Acronym to DoDiff
command -nargs=0 DD exec substitute(join(filter(split(getline(line("."))), 'v:val !~ "^-"')), '\v\C^(diff\s+([^ ]+)\s+([^ ]+))|(.*)$', '\=len(submatch(1)) ? "tabnew ".submatch(2). " | vertical rightbelow diffsplit ".submatch(3) : "echo \"Not a diff command under cursor\""', '')

nmap <buffer> <leader>d :DD<CR>

" Next change
nmap <buffer> ]c :echo search("^diff")<CR>
nmap <buffer> [c :echo search("^diff", "b")<CR>

" Next section
nmap <buffer> ]] :echo search("^diff")<CR>
nmap <buffer> [[ :echo search("^diff", "b")<CR>

" Next paragraph
nmap <buffer> } :echo search('\v^diff\|^[@0-9]')<CR>
nmap <buffer> { :echo search('\v^diff\|^[@0-9]', "b")<CR>

