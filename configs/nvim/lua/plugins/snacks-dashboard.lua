return {
  "folke/snacks.nvim",
  priority = 1000,
  lazy = false,
  opts = {
    dashboard = {
      enabled = true,
      preset = {
        header = [[
+------------------------------------------------------+
|                                                      |
|         ________________  _________ ____  ___        |
|         \__    ___/  _  \ \_   ___ \\   \/  /        |
|           |    | /  /_\  \/    \  \/ \     /         |
|           |    |/    |    \     \____/     \         |
|           |____|\____|__  /\______  /___/\  \_       |
|                         \/        \/      \  /       |
|                                            \/        |
+------------------------------------------------------+
|         - You didn't wake up to be mediocre          |
+------------------------------------------------------+
]],
        keys = {
          {
            icon = " ",
            key = "f",
            desc = "Find File",
            action = function()
              require("lazy").pick()
            end,
          },
          { icon = " ", key = "n", desc = "New File", action = "ene | startinsert" },
          {
            icon = " ",
            key = "r",
            desc = "Recent Files",
            action = function()
              require("lazy").pick("oldfiles")
            end,
          },
          {
            icon = " ",
            key = "g",
            desc = "Find Text",
            action = function()
              require("lazy").pick("live_grep")
            end,
          },
          {
            icon = " ",
            key = "c",
            desc = "Config",
            action = function()
              require("lazy").pick_config_files()
            end,
          },
          {
            icon = " ",
            key = "s",
            desc = "Restore Session",
            action = function()
              require("persistence").load()
            end,
          },
          { icon = " ", key = "x", desc = "Lazy Extras", action = "LazyExtras" },
          { icon = "󰒲 ", key = "l", desc = "Lazy", action = "Lazy" },
          {
            icon = " ",
            key = "q",
            desc = "Quit",
            action = function()
              vim.api.nvim_input("<cmd>qa<cr>")
            end,
          },
        },
        footer = function()
          local stats = require("lazy").stats()
          local ms = math.floor(stats.startuptime * 100 + 0.5) / 100
          local lines = {
            "",
            "⚡ Neovim loaded " .. stats.loaded .. "/" .. stats.count .. " plugins in " .. ms .. "ms",
          }
          local fortune = require("fortune").get_fortune()
          for _, f in ipairs(fortune) do
            table.insert(lines, f)
          end
          return table.concat(lines, "\n")
        end,
      },
    },
  },
}
