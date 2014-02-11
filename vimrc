"set tags=~/linux-uek3-3.8.git/tags

set tags=tags;
set ai
set cindent
set textwidth=80
set noexpandtab
set backup
set backspace=indent,eol,start
set autoread
set visualbell
set virtualedit=block
set sessionoptions=buffers,curdir,folds,options,tabpages

set laststatus=2
set restorescreen

"syntax off
set background=light
"colorscheme delek
set t_Co=256


highlight clear
if exists("syntax_on")
    syntax reset
endif

map <C-b> gq}

let g:colors_name = "delek1"

hi Normal cterm=NONE ctermfg=237  ctermbg=255

hi Comment      ctermfg=115 cterm=bold

hi Constant     ctermfg=80 cterm=bold
hi String   	ctermfg=72 cterm=bold
hi Boolean	ctermfg=88
hi Number       ctermfg=132

hi Identifier   ctermfg=160
hi Function     ctermfg=132

hi Statement    ctermfg=19 cterm=bold
hi Keyword      ctermfg=57

hi PreProc      ctermfg=151  cterm=bold

hi Type         ctermfg=116 cterm=bold
hi StorageClass ctermfg=19 cterm=bold

hi Special      ctermfg=64

hi Ignore       ctermfg=255
hi Error        ctermfg=196             ctermbg=255     cterm=none
hi Search       ctermfg=131             ctermbg=255 cterm=NONE
hi Todo         ctermfg=136             ctermbg=255     cterm=NONE

hi VimError         ctermfg=160          ctermbg=16
hi VimCommentTitle  ctermfg=110
hi qfLineNr         ctermfg=16           ctermbg=46        cterm=NONE
hi pythonDecorator ctermfg=208   ctermbg=255 cterm=NONE
hi Cursor       ctermfg=255             ctermbg=16              cterm=NONE
hi CursorColumn ctermfg=NONE            ctermbg=255             cterm=NONE
hi CursorIM     ctermfg=255             ctermbg=16              cterm=NONE
hi CursorLine   ctermfg=NONE            ctermbg=254             cterm=NONE
hi lCursor      ctermfg=255             ctermbg=16              cterm=NONE
hi DiffAdd      ctermfg=16              ctermbg=48              cterm=NONE
hi DiffChange   ctermfg=16              ctermbg=153             cterm=NONE
hi DiffDelete   ctermfg=16              ctermbg=203             cterm=NONE
hi DiffText     ctermfg=16              ctermbg=226             cterm=NONE
hi Directory    ctermfg=21              ctermbg=255             cterm=NONE
hi ErrorMsg     ctermfg=160             ctermbg=NONE            cterm=NONE
hi FoldColumn   ctermfg=24              ctermbg=252             cterm=NONE
hi Folded       ctermfg=24              ctermbg=252             cterm=NONE
hi IncSearch    ctermfg=255             ctermbg=160             cterm=NONE
hi LineNr       ctermfg=253             ctermbg=110             cterm=NONE
hi NonText      ctermfg=110             ctermbg=255             cterm=NONE
hi Pmenu        ctermfg=fg              ctermbg=195             cterm=NONE
hi PmenuSbar    ctermfg=255             ctermbg=153             cterm=NONE
hi PmenuSel     ctermfg=255             ctermbg=21              cterm=NONE
hi PmenuThumb   ctermfg=111             ctermbg=255             cterm=NONE
hi SignColumn   ctermfg=110             ctermbg=254             cterm=NONE
hi SpecialKey   ctermfg=255             ctermbg=144             cterm=NONE
hi SpellBad     ctermfg=16              ctermbg=229             cterm=NONE
hi SpellCap     ctermfg=16              ctermbg=231             cterm=NONE
hi SpellLocal   ctermfg=16              ctermbg=231             cterm=NONE
hi SpellRare    ctermfg=16              ctermbg=226             cterm=NONE
hi StatusLine   ctermfg=255             ctermbg=24              cterm=NONE
hi StatusLineNC ctermfg=253             ctermbg=110             cterm=NONE
hi Title        ctermfg=75              ctermbg=255             cterm=NONE
hi VertSplit    ctermfg=255             ctermbg=24              cterm=NONE
hi Visual       ctermfg=255             ctermbg=153             cterm=NONE
hi WildMenu     ctermfg=16              ctermbg=117             cterm=NONE


highlight ExtraWhitespace ctermbg=red guibg=red
match ExtraWhitespace /\s\+$/
autocmd BufWinEnter * match ExtraWhitespace /\s\+$/
autocmd InsertEnter * match ExtraWhitespace /\s\+\%#\@<!$/
autocmd InsertLeave * match ExtraWhitespace /\s\+$/
autocmd BufWinLeave * call clearmatches()

if exists('+colorcolumn')
    set colorcolumn=80
else
    au BufWinEnter * let w:m2=matchadd('ErrorMsg', '\%>80v.\+', -1)
endif


set spelllang=en
set spellfile=$HOME/.spellfile.en.add
