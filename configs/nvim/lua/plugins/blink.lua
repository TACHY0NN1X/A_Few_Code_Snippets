return {
  "saghen/blink.cmp",
  opts = {
    keymap = {
      preset = "super-tab", -- Tab completes + Shift-Tab goes back
    },
    completion = {
      menu = {
        border = "rounded",
        draw = {
          treesitter = { "lsp" },
        },
      },
      documentation = {
        window = {
          border = "rounded",
        },
        auto_show = true,
        auto_show_delay_ms = 200,
      },
      ghost_text = {
        enabled = vim.g.ai_cmp,
      },
      list = {
        selection = {
          preselect = false, -- do not auto highlight randomly…
          auto_insert = true, -- …instead insert selected / first item on Tab
        },
      },
    },
  },
}
