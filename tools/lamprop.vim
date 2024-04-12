" Vim syntax file
" Language: lamprop
" Maintainer: R.F. Smith <rsmith@xs4all.nl>
" Created: 2015-11-01 12:32:18 +0100
" Last modified: 2024-04-12T13:42:51+0200

" Quit when a (custom) syntax file was already loaded.
if exists("b:current_syntax")
    finish
endif

syn case ignore
syn spell toplevel

syn match lampropComment "^.*$" contains=@Spell
syn match lampropStart "^[frtmls]:"
syn match lampropNumber "\<[+-]\?\d\+"
syn match lampropNumber "\<[+-]\?\d\+\.\d\+"
syn match lampropNumber "\<[+-]\?\d\+\%(\.\d\+\)\?\%([eE][+-]\?\d\+\)"

hi def link lampropComment Comment
hi def link lampropNumber Number
hi def link lampropStart Function

let b:current_syntax = "lamprop"
