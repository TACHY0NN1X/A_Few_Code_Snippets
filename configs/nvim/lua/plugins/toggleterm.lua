return {
  "akinsho/toggleterm.nvim",
  version = "*",
  config = function()
    require("toggleterm").setup({
      direction = "float", -- floating terminal
      float_opts = {
        border = "single", -- simple border
        winblend = 0, -- opaque
      },
      hide_numbers = true, -- hide line numbers
      start_in_insert = true, -- start in insert mode
      close_on_exit = false, -- terminal stays open after commands finish
    })

    -- keybinding to toggle the terminal
    vim.keymap.set("n", "<leader>t", "<cmd>ToggleTerm<CR>", { silent = true, noremap = true })
    vim.keymap.set("t", "<leader>t", "<C-\\><C-n><cmd>ToggleTerm<CR>", { silent = true, noremap = true })
  end,
}
