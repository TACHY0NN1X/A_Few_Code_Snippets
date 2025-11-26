-- =====================================================================
-- 💤 init.lua — Neovim configuration using LazyVim
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
local global = vim.g -- Global
local map = vim.keymap.set

-- UI ------------------------------------------------------------------

-- Gruvbox Settings
global.gruvbox_material_background = "hard"
global.gruvbox_material_foreground = "original"
global.gruvbox_material_enable_italic = 1
global.gruvbox_material_enable_bold = 1

vim.cmd.colorscheme("gruvbox-material")

opt.number = true -- Show absolute line numbers
opt.relativenumber = false -- Disable relative line numbers
opt.cursorline = true -- Highlight current line
opt.termguicolors = true -- Enable 24-bit RGB color in terminal
opt.signcolumn = "yes" -- Always show sign column (for git/lsp)
opt.wrap = false -- No line wrapping
opt.scrolloff = 8 -- Keep 8 lines visible above/below cursor
opt.list = true -- Show whitespace

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

-- Language ------------------------------------------------------------
opt.spell = true
opt.spelllang = "en_gb,en_us"

-- ---------------------------------------------------------------------
-- 🪄 3. Useful Keymaps
-- ---------------------------------------------------------------------
-- You can add quick custom mappings below.
-- LazyVim already sets up good defaults, so add only unique ones here.
-- ---------------------------------------------------------------------

map("n", "<leader>h", ":nohlsearch<CR>", { desc = "Clear search highlight" })

-- ---------------------------------------------------------------------
-- 🌈 4. Extra Tweaks
-- ---------------------------------------------------------------------
-- These are optional but nice to have.
-- ---------------------------------------------------------------------
opt.showcmd = true -- Show partial commands in status line
opt.ruler = true -- Show line and column number of cursor
opt.laststatus = 3 -- Global status line
opt.mouse = "a" -- Enable mouse

-- ---------------------------------------------------------------------
-- ⚠️ Diagnostics
-- ---------------------------------------------------------------------
vim.diagnostic.config({
  virtual_text = { severity = vim.diagnostic.severity.ERROR },
  signs = { severity = vim.diagnostic.severity.ERROR },
  underline = { severity = vim.diagnostic.severity.ERROR },
})

global.vimtex_quickfix_ignore_filters = { "warning" }

-- Plugins
global.ai_cmp = true

-- --------------------------------------------------------------------
-- Neovide Setup
-- --------------------------------------------------------------------
if vim.g.neovide then
  opt.guifont = "FantasqueSansM Nerd Font:h13"
  vim.g.neovide_scale_factor = 1.0
end
