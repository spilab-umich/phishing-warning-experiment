//names in the phishnet
var names = ["https://www.chase-banking.us/", "https://www.venmo-login.com/", "https://www.website-welcome.ru/", "https://www.yourorders-review.com/", "https://www.yahoo-password.com.br/"];
var hover_time_limit = 250;

function checkLinks(condition_group) {
    // Add a click listener to all anchors (inbox and email)
    // This will not put a click listener on any warning links
    $('a').each(function() {
        addclicklistener($(this));
    });

    // Add a hover listener with time to all anchors in the email container
    // This will not put a hover listener on any warnings
    $('#email_container a').each(function() {
        addHoverListener($(this));
    });

    //go through each anchor in the email
    // throw the warnings on phish
    $('#email_container a').each(function() {
        var start, end;
        // try to use "propogation" to handle this click listener
        var raw_link = $(this).attr("href");
        //if the raw link is in our phish-net
        if (names.indexOf(raw_link) > -1) {
            var delay, trigger, text, warning, correct_link, options, raw_link, clean_link;
            // Render a warning on this link
            renderWarning(condition_group, $(this));
        }
    });

    function renderWarning(condition_group, element) {
        raw_link = element.attr('href');
        clean_link = extractHostname(raw_link);
        //turn the suspect link's data-toggle attribute to 'tooltip'
        element.attr('data-toggle', 'tooltip');
        loadWarning(condition_group, element);
        throwWarning(options, condition_group);
    }

    function loadWarning(condition_group, element) {
        //clean the href
        var warning_header = "FAKE WEBSITE, DON'T CLICK!";
        var text = '<div class="fa fa-exclamation-triangle icon-sm fa-2x"></div><div class="warning-header">' + warning_header + '</div><div class="warning-text">Link goes to: <a class="warning-link" href="' + raw_link + '" id=-100 target="_blank">' + clean_link + '</a></div>';
        var template = '<div class="tooltip" role="tooltip"><div class="tooltip-arrow"></div><div class="tooltip-inner warning"></div></div>';
        //apply warning according to condition group
        //CG1: on-load, no forced choice
        if (condition_group == 1) {
            //add a close button for manual trigger
            trigger = 'manual';
            text = '<a label="close_button" class = "close-button"></a>' + text;
        }

        //CG1: on-load, forced choice
        else if (condition_group == 2) {
            //add a close button for manual trigger
            trigger = 'manual';
            text = '<a label="close_button" class = "close-button"></a>' + text;
            element.css('cursor', 'not-allowed');
            var href = element.attr('href');
            element.removeAttr('href').attr('label', href);
        }

        // CG3: on-hover, no forced choice
        else if (condition_group == 3) {
            trigger = 'manual';
        }

        // CG4: on hover, forced choice
        else if (condition_group == 4) {
            //add a close button for manual trigger
            trigger = 'manual';
            //Move the href to the label
            var href = element.attr('href');
            element.removeAttr('href').attr('label', href);
            element.css('cursor', 'not-allowed');
        }

        // CG5: banner
        else if (condition_group == 5) {
            trigger = ""
            // Construct the banner warning between the email header and email body
            warning_header = "THIS EMAIL CONTAINS A LINK TO A FAKE WEBSITE, DON'T CLICK!"
            text = '<div class="media warning banner"><div class="warning-header"><div class="fa fa-exclamation-triangle icon-sm fa-2x"></div>' + warning_header + '</div><br><div class="warning-text">Link goes to: <a class="warning-link" href="' + raw_link + '" id=-100 target="_blank">' + clean_link + '</a></div></div>';
            $('.heading').after(text);
            handleAction('warning shown', 'warning');
            $('.warning-link').each(function() {
                // Add click listener to CG5 warning link
                addclicklistener($(this));
                // Add hover listener to CG5 warning-links
                addHoverListener($(this));
            });
        }

        //CG6: browser
        else if (condition_group == 6) {
            // Construct browser warning
            trigger = ""
            warning_header = "FAKE WEBSITE AHEAD";
            var suspect_link = "<a class = 'warning-link' href ='" + raw_link + "' id=-100 target='_blank'> here </a>";
            var warning_text = "You are about to enter the webpage <strong>" + clean_link + "</strong>.<br>Click " + suspect_link + " to continue.<br><a label='close_button' class='warning-link'>Return to safety</a>";
            var href = element.attr('href');
            element.removeAttr('href').attr('label', href);
            text = '<div class = "warning-content"><div class="warning-wrapper"><div class="fa fa-exclamation-triangle icon-sm fa-5x"></div><div class="warning-header">' + warning_header + '</div><div class="warning-text">' + warning_text + '</div></div>';
            $('.warning, .full').append(text);
            // On click, show the warning and send a log
            element.on('click', function() {
                $('.warning, .full').css('display', "block");
                handleAction('warning shown', 'warning');
            });
            // If the warning link is clicked, dismiss the warning
            $('.warning-link').on("click", function() {
                $('.warning, .full').css('display', "none");
                // handleAction('warning closed', 'warning');
            });

            // Do things to the CG6 warning links (Back to safety and phish website)
            $('.warning-link').each(function() {
                // Add click listener to CG6 warning links
                addclicklistener($(this));
                // Add hover listener to CG6 warning-links
                addHoverListener($(this));
            });
        }

        //options for tooltip
        options = {
            placement: 'bottom',
            html: true,
            title: text,
            trigger: trigger,
            template: template,
        }
    }


    function throwWarning(options, condition_group) {
        //render the tooltip warnings
        if (condition_group <= 4 & condition_group > 0) {
            $("[data-toggle='tooltip']").tooltip(options);
        }

        // Do things when the tooltip-warnings are rendered  (CGs 1-4)
        $('[data-toggle="tooltip"]').on("shown.bs.tooltip", function() {
            handleAction('warning shown', 'warning');
            // Add listeners to warning links in tooltip warnings
            $('.warning-link').each(function() {
                addclicklistener($(this));
                // Add hover listener to warning links in tooltip warnings
                addHoverListener($(this));
            });
            initializeCloseButton();
        });
        // Forced choice+on-load should be toggled on click
        // show the warning if the phish link is clicked
        if (condition_group == 2) {
            $('[data-toggle="tooltip"]').on("click", function() {
                $("[data-toggle='tooltip']").tooltip('show');
            });
        }
        // initialize the close button on tooltip show
        function initializeCloseButton() {
          // Add click listeners to close buttons
          $("a.close-button").each(function(){
            var _this = $(this);
            addclicklistener(_this);
          });
            //initialize the close button
            $("a.close-button").on('click', function() {
                $("[data-toggle='tooltip']").tooltip('hide');
            });
        }
        //show on-load warnings
        if (condition_group == 2 | condition_group == 1) {
            //show tooltips on load
            $("[data-toggle='tooltip']").tooltip("toggle");
        }
        if (condition_group == 4 | condition_group == 3) {
            $("[data-toggle='tooltip']").tooltip().on("mouseenter", function() {
            var _this = this;
                $(this).tooltip("show");
            }).on("mouseleave", function() {
                var _this = this;
                // Check to see if the tooltop or link is hovered every 500ms
                var refreshInterval = setInterval(function() {
                  // if the tooltip or link are not hovered over, clear the interval check and dismiss the tooltip
                    if (!$(".tooltip-inner:hover").length && !$("[data-toggle='tooltip']:hover").length) {
                        $(_this).tooltip("hide");
                        clearInterval(refreshInterval);
                    }
                }, 500);
            });
          }
      }
}

function addclicklistener(_this) {
    _this.on('click', function() {
        handleAction(_this, 'click');
    });
}

function addHoverListener(_this) {
    _this.hover(function() {
        start = new Date();
    }, function() {
        end = new Date();
        var time = end - start;
        if (time >= hover_time_limit) {
          handleAction($(this), 'hover', time);
        }
    });
}

function extractHostname(url) {
    var hostname;
    //find & remove protocol (http, ftp, etc.) and get hostname
    if (url.indexOf("://") > -1) {
        hostname = url.split('/')[2];
    } else {
        hostname = url.split('/')[0];
    }
    //find & remove port number
    hostname = hostname.split(':')[0];
    //find & remove "?"
    hostname = hostname.split('?')[0];
    return hostname;
}
