-- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
--
-- Autor = Shen Blaskowitz
-- Inpiracions = https://github.com/LazyVim/LazyVim
-- Followme = https://github.com/Shentxt
--
-- ██╗███╗   ██╗██╗████████╗
-- ██║████╗  ██║██║╚══██╔══╝
-- ██║██╔██╗ ██║██║   ██║
-- ██║██║╚██╗██║██║   ██║
-- ██║██║ ╚████║██║   ██║
-- ╚═╝╚═╝  ╚═══╝╚═╝   ╚═╝
--
-- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

-- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
--                  Comand
--
-- Mason = Install Plug lenguaj
-- Lazy = Chek Integrity
-- CheckHealth = Chek Lazy
--
-- write any letter you want to know its combination and what it does
-- used space = all keys
-- example = W
--
-- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

-- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
--                 Executed All Files
--
-- this folder is used to load the necessary files needed by hyprlan
-- each name indicates what the file is about
-- if you need information go to the page of nvim and lua
--
-- documentacion
-- - - - - - -
-- wiki: https://www.vim.org/
-- wiki: https://www.lua.org/docs.html
--
-- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

-- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
--                 Search Files Configuration
-- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

-- bootstrap nvim and your plugins
require "config.lazy"

-- Scripts of nvim
require "scripts.autovim"
require "scripts.autoresize"
require "scripts.autospelling"
require "scripts.linehighlight"
require "scripts.lastread"
require "scripts.enablekeys"
