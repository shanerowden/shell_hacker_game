//   Toggles terminal

function closePanel(divs, except) {
    for (let i = 0; i < divs.length; i++) {

      if (divs[i] != except) {
        if ($(divs[i]).is(":visible")) {

            $(divs[i]).toggle({
              duration: 1000,
              });

          };
        };
      };
  };

let listedPanels = ['#fim-editor', '#vanilla-terminal']

  $(document).ready(function() {

      $("#open-terminal").click(function() {

          $("#vanilla-terminal").toggle({
              duration: 1000,
            });
          $("#terminal-option-listing-open").toggle({
            duration: 1000,
            });
          $("#terminal-option-listing-close").toggle({
            duration: 1000,
            });
          closePanel(listedPanels, "#vanilla-terminal");
          });
        });
