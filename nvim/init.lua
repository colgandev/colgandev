-- Bootstrap lazy.nvim
local lazypath = vim.fn.stdpath "data" .. "/lazy/lazy.nvim"
if not (vim.uv or vim.loop).fs_stat(lazypath) then
    local lazyrepo = "https://github.com/folke/lazy.nvim.git"
    local out = vim.fn.system { "git", "clone", "--filter=blob:none", "--branch=stable", lazyrepo, lazypath }
    if vim.v.shell_error ~= 0 then
        vim.api.nvim_echo({
            { "Failed to clone lazy.nvim:\n", "ErrorMsg" },
            { out, "WarningMsg" },
            { "\nPress any key to exit..." },
        }, true, {})
        vim.fn.getchar()
        os.exit(1)
    end
end
vim.opt.rtp:prepend(lazypath)

-- Leader key setup
vim.g.mapleader = ","
vim.g.maplocalleader = "\\"

-- Enable filetype plugins and syntax highlighting
vim.cmd [[
  filetype plugin on
  filetype indent on
  syntax on
]]

-- Basic editing preferences
vim.opt.shortmess = vim.o.shortmess .. "c"
vim.opt.hidden = true
vim.opt.whichwrap = "b,s,<,>,[,],h,l,~"
vim.opt.pumheight = 10
vim.opt.encoding = "utf-8"
vim.opt.ruler = true
vim.opt.showmode = true
vim.opt.showcmd = true
vim.opt.fileencoding = "utf-8"
vim.opt.cmdheight = 1
vim.opt.splitbelow = true
vim.opt.splitright = true
vim.opt.termguicolors = true
vim.opt.conceallevel = 0
vim.opt.backup = false
vim.opt.writebackup = false
vim.opt.updatetime = 250
vim.opt.timeoutlen = 300
vim.opt.clipboard = "unnamedplus"

-- Search settings
vim.opt.incsearch = true
vim.opt.ignorecase = true
vim.opt.smartcase = true
vim.opt.hlsearch = true

-- Display settings
vim.opt.numberwidth = 3
vim.opt.scrolloff = 3
--vim.opt.sidescrolloff = 5
vim.opt.mouse = "a"
vim.opt.wrap = true
vim.opt.backspace = "2"
vim.opt.linebreak = true
vim.opt.textwidth = 0
vim.opt.number = true
vim.opt.cursorline = true
vim.opt.signcolumn = "yes"

-- Indentation and tabs
vim.opt.tabstop = 4
vim.opt.softtabstop = 4
vim.opt.shiftwidth = 4
vim.opt.foldenable = false
--vim.opt.indentexpr = ''
--vim.opt.autoindent = true
--vim.opt.smartindent = false
--vim.opt.cindent = false
vim.opt.cinkeys = ""
vim.opt.shiftround = true
vim.opt.expandtab = true
vim.opt.showmatch = true

-- History and undo
vim.opt.history = 10000
vim.opt.undolevels = 10000
vim.opt.errorbells = false

-- Auto-reading files
vim.opt.autoread = true
vim.opt.swapfile = false

-- Initialize Lazy with plugin specs
require("lazy").setup {
    { "ellisonleao/gruvbox.nvim", priority = 1000, config = true },
    {
        "nvim-tree/nvim-tree.lua",
        version = "*",
        lazy = false,
        dependencies = {
            "nvim-tree/nvim-web-devicons",
        },
    },
    {
        "nvim-telescope/telescope.nvim",
        tag = "0.1.8",
        dependencies = { "nvim-lua/plenary.nvim" },
    },
    {
        "stevearc/oil.nvim",
        opts = {},
        -- Optional dependencies
        dependencies = { "nvim-tree/nvim-web-devicons" }, -- use if you prefer nvim-web-devicons
        -- Lazy loading is not recommended because it is very tricky to make it work correctly in all situations.
        lazy = false,
    },
    {
        "nvim-treesitter/nvim-treesitter",
        build = ":TSUpdate",
        config = function()
            local configs = require "nvim-treesitter.configs"

            configs.setup {
                ensure_installed = { "lua", "vim", "vimdoc", "query", "javascript", "html", "python" },
                highlight = { enable = true },
                indent = { enable = true },
            }
        end,
    },
    {
        "davidmh/mdx.nvim",
        config = true,
        dependencies = { "nvim-treesitter/nvim-treesitter" },
    },
    {
        "joshuavial/aider.nvim",
        opts = {
            -- your configuration comes here
            -- if you don't want to use the default settings
            auto_manage_context = true, -- automatically manage buffer context
            default_bindings = true, -- use default <leader>A keybindings
            debug = false, -- enable debug logging
        },
    },
}

-- Color scheme
vim.g.gruvbox_contrast_dark = "hard"
vim.g.gruvbox_contrast_light = "hard"
vim.cmd "colorscheme gruvbox"
vim.opt.background = "dark"
--vim.opt.background = 'light'

require "mde"

-- Create an autocmd group for all autocommands
local augroup = vim.api.nvim_create_augroup("UserAutocommands", { clear = true })

-- Check for external file changes
vim.api.nvim_create_autocmd({ "FocusGained", "BufEnter" }, {
    group = augroup,
    pattern = "*",
    command = "checktime",
})

-- Auto-save on focus lost
vim.api.nvim_create_autocmd({ "FocusLost" }, {
    group = augroup,
    pattern = "*",
    command = "silent! wa",
})

-- Beancount-specific configurations
vim.api.nvim_create_autocmd("FileType", {
    group = augroup,
    pattern = "beancount",
    callback = function()
        vim.keymap.set("i", ".", ".<C-\\><C-O>:AlignCommodity<CR>", { buffer = true })
        vim.keymap.set("n", "<leader>=", ":AlignCommodity<CR>", { buffer = true })
        vim.keymap.set("v", "<leader>=", ":AlignCommodity<CR>", { buffer = true })
    end,
})

-- Set terminal title to show current file path
local function set_terminal_title()
    local hostname = vim.fn.hostname()
    local username = vim.fn.expand "$USER"
    local filepath = vim.fn.expand "%:p"
    local titlestring = username .. "@" .. hostname .. ":" .. filepath
    vim.opt.titlestring = titlestring
    vim.opt.title = true
end

-- Auto-update terminal title
vim.api.nvim_create_autocmd({ "BufEnter", "BufWritePost" }, {
    group = augroup,
    callback = function()
        set_terminal_title()
    end,
})
-- Helper functions for mapping keys
local function map(mode, shortcut, command)
    vim.api.nvim_set_keymap(mode, shortcut, command, { noremap = true, silent = true })
end

local function nmap(shortcut, command)
    map("n", shortcut, command)
end
local function imap(shortcut, command)
    map("i", shortcut, command)
end
local function vmap(shortcut, command)
    map("v", shortcut, command)
end
local function cmap(shortcut, command)
    map("c", shortcut, command)
end
local function tmap(shortcut, command)
    map("t", shortcut, command)
end

-- Save shortcuts
nmap("<C-s>", ":w<CR>")
imap("<C-s>", "<Esc>:w<CR>")
nmap("<leader><space>", "<cmd>wa<cr>")
nmap("<space><space>", "<cmd>wa<cr>")

-- Delete word backward
imap("<C-BS>", "<C-W>")
imap("<C-H>", "<C-W>") -- For terminal compatibility

-- Escape shortcuts
--nmap('<c-c>', '<esc>')
imap("<c-c>", "<esc>")
vmap("<c-c>", "<esc>")

-- Whitespace removal
nmap("<leader>ws", ":%s/\\s\\+$//e<CR>")

-- Command line navigation
cmap("<c-a>", "<home>")
cmap("<c-e>", "<end>")
cmap("<c-f>", "<right>")
cmap("<c-b>", "<left>")
cmap("<m-f>", "<c-right>")
cmap("<m-b>", "<c-left>")
cmap("<c-k>", "<c-o>C")

-- File explorer
nmap("<leader>nn", ":NvimTreeToggle<CR>")
nmap("<leader>nf", ":NvimTreeFindFile<CR>")

-- Date/timestamp insertion
nmap(
    "<leader>d",
    'A [[<cr>    ---<cr>    ---<cr>]]<esc><up><up>o    <esc>!!date +"timestamp: \\%Y-\\%m-\\%dT\\%H:\\%M:\\%S\\%:z"<cr>'
)

-- Yank to end of line (consistent with D and C)
nmap("Y", "y$")

-- Center view after scrolling
nmap("<C-l>", "<C-l>zz")

-- Colemak navigation changes
nmap("t", "gj")
nmap("n", "gk")
nmap("s", "l")
nmap("l", "nzzzv")
nmap("j", "t")
nmap("k", "s")
nmap("T", "}")
nmap("N", "{")
nmap("L", "Nzzzv")
nmap("J", "T")
--nmap('K', 'S')
nmap("S", "$")
nmap("H", "^")

-- Visual mode mappings
vmap("t", "gj")
vmap("n", "gk")
vmap("s", "l")
vmap("l", "n")
vmap("j", "t")
vmap("k", "s")
vmap("T", "}")
vmap("N", "{")
vmap("L", "N")
vmap("J", "T")
vmap("K", "S")
vmap("S", "$")
vmap("H", "^")

-- Clear search highlighting
nmap("<leader>h", "<cmd>nohl<cr>")

-- Join lines with -
nmap("-", "J")
vmap("-", "J")

-- Format paragraph
nmap("Q", "gqap")

-- Window navigation with Space
nmap("<space>", "<c-w>")
nmap("<space>t", "<C-w>j")
nmap("<space>T", "<C-w>J")
nmap("<space>n", "<C-w>k")
nmap("<space>N", "<C-w>K")
nmap("<space>s", "<C-w>l")
nmap("<space>S", "<C-w>L")
nmap("<space>j", "<C-w>t")
nmap("<space>J", "<C-w>T")
nmap("<space>k", "<C-w>n")
nmap("<space>K", "<C-w>N")
nmap("<space>l", "<C-w>s")
nmap("<space>L", "<C-w>S")

-- Color scheme toggle
nmap("<leader>cl", ":set bg=light<cr>")
nmap("<leader>cd", ":set bg=dark<cr>")

-- File operations
nmap("<leader>cx", ":!chmod +x %<cr>")
nmap("<leader>xx", "<cmd><cr><cmd>source %<cr>")

-- Scroll multiple lines
nmap("<C-e>", "3<C-e>")
nmap("<C-y>", "3<C-y>")

-- Create undo points
imap(",", ",<c-g>u")
imap(".", ".<c-g>u")
imap("!", "!<c-g>u")
imap("?", "?<c-g>u")

-- Quickfix navigation
nmap("<leader>cn", "<cmd>cnext<cr>")
nmap("<leader>cp", "<cmd>cprevious<cr>")

-- Telescope shortcuts
nmap("<C-p>", "<cmd>Telescope find_files<cr>")
nmap("<C-g>", "<cmd>Telescope live_grep<cr>")
--nmap('<C-?>', '<cmd>Telescope help_tags<cr>')
--nmap('<leader>rf', ':Telescope find_files<cr>')
--nmap('<leader>rg', ':Telescope live_grep<cr>')
--nmap('<leader>rh', ':Telescope help_tags<cr>')
local telescope = require "telescope"

-- Configure telescope
telescope.setup {
    defaults = {
        prompt_prefix = "❯ ",
        selection_caret = "❯ ",
        path_display = { "truncate" },
        selection_strategy = "reset",
        sorting_strategy = "ascending",
        layout_strategy = "horizontal",
        layout_config = {
            horizontal = {
                prompt_position = "top",
                preview_width = 0.55,
                results_width = 0.8,
            },
            vertical = {
                mirror = false,
            },
            width = 0.87,
            height = 0.80,
            preview_cutoff = 120,
        },
    },
}
local nvim_tree = require "nvim-tree"

-- Configure nvim-tree
nvim_tree.setup {
    sort_by = "case_sensitive",
    view = {
        width = 30,
    },
    renderer = {
        group_empty = true,
    },
    filters = {
        dotfiles = false,
    },
}

-- open tree on startup
--local nvim_tree_api = require "nvim-tree.api"
--nvim_tree_api.tree.open()
