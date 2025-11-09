-- =====================================================================
-- 💤 init.lua — Neovim configuration using LazyVim
-- =====================================================================
-- This file sets up basic editor behavior and integrates LazyVim plugin
-- management. It’s minimal, opinionated, and heavily commented so you
-- can easily tweak it later.
-- =====================================================================

-- ---------------------------------------------------------------------
-- 🧩 1. Load LazyVim
-- ---------------------------------------------------------------------
-- LazyVim is a prebuilt, modular Neovim config using lazy.nvim.
-- It automatically installs itself and manages plugins cleanly.
-- ---------------------------------------------------------------------
require("config.lazy")

-- ---------------------------------------------------------------------
-- ⚙️ 2. Core Editor Settings
-- ---------------------------------------------------------------------
-- These are equivalent to `:set` options in traditional vimscript.
-- For readability, all options are grouped logically.
-- ---------------------------------------------------------------------
local opt = vim.opt -- Shorthand

-- UI ------------------------------------------------------------------
opt.number = true -- Show absolute line numbers
opt.relativenumber = false -- Disable relative line numbers
opt.cursorline = true -- Highlight current line
opt.termguicolors = true -- Enable 24-bit RGB color in terminal
opt.signcolumn = "yes" -- Always show sign column (for git/lsp)
opt.wrap = false -- No line wrapping
opt.scrolloff = 8 -- Keep 8 lines visible above/below cursor

-- Indentation ---------------------------------------------------------
opt.tabstop = 3 -- A tab equals 3 spaces
opt.shiftwidth = 3 -- Indent by 3 spaces
opt.softtabstop = 3 -- Pressing <Tab> inserts 3 spaces
opt.expandtab = true -- Convert tabs to spaces
opt.smartindent = true -- Auto-indent new lines smartly

-- Search --------------------------------------------------------------
opt.ignorecase = true -- Ignore case when searching...
opt.smartcase = true -- ...unless capital letters are used
opt.incsearch = true -- Show matches as you type
opt.hlsearch = true -- Highlight all matches

-- Editing -------------------------------------------------------------
opt.clipboard = "unnamedplus" -- Use system clipboard
opt.undofile = true -- Persistent undo between sessions
opt.backup = false -- Don’t create backup files
opt.swapfile = false -- Don’t use swap files
opt.autoread = true -- Auto-reload file if changed externally
opt.confirm = true -- Ask to save changes before closing

-- Timing --------------------------------------------------------------
opt.timeoutlen = 400 -- Faster key sequence timeout
opt.updatetime = 200 -- Faster updates for diagnostics

-- Splits --------------------------------------------------------------
opt.splitbelow = true -- Horizontal splits open below
opt.splitright = true -- Vertical splits open to the right

-- ---------------------------------------------------------------------
-- 🪄 3. Useful Keymaps
-- ---------------------------------------------------------------------
-- You can add quick custom mappings below.
-- LazyVim already sets up good defaults, so add only unique ones here.
-- ---------------------------------------------------------------------
local map = vim.keymap.set

map("n", "<leader>w", ":w<CR>", { desc = "Save file" })
map("n", "<leader>q", ":q<CR>", { desc = "Quit window" })
map("n", "<leader>h", ":nohlsearch<CR>", { desc = "Clear search highlight" })

-- ---------------------------------------------------------------------
-- 🌈 4. Extra Tweaks
-- ---------------------------------------------------------------------
-- These are optional but nice to have.
-- ---------------------------------------------------------------------
vim.cmd([[
  set showcmd              " Show partial commands in status line
  set ruler                " Show line and column number of cursor
  set laststatus=3         " Global status line
  set mouse=a              " Enable mouse
]])

vim.diagnostic.config({
  virtual_text = { severity = vim.diagnostic.severity.ERROR },
  signs = { severity = vim.diagnostic.severity.ERROR },
  underline = { severity = vim.diagnostic.severity.ERROR },
})

vim.cmd("colorscheme tokyonight-night")

require("lspconfig").ltex.setup({
  settings = {
    ltex = {
      checkFrequency = "save", -- or "edit" / "manual"
    },
  },
})
