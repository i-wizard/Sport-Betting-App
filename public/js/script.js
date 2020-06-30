"use strict";
(function () {
    var userAgent = navigator.userAgent.toLowerCase(), initialDate = new Date(), $document = $(document),
        $window = $(window), $html = $("html"), $body = $("body"), isDesktop = $html.hasClass("desktop"),
        isRtl = $html.attr("dir") === "rtl",
        isIE = userAgent.indexOf("msie") !== -1 ? parseInt(userAgent.split("msie")[1], 10) : userAgent.indexOf("trident") !== -1 ? 11 : userAgent.indexOf("edge") !== -1 ? 12 : false,
        isMobile = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent),
        windowReady = false, isNoviBuilder = false, preloaderAnimateionDuration = 300, loaderTimeoutId, plugins = {
            preloader: $("#preloader"),
            bootstrapTooltip: $("[data-toggle='tooltip']"),
            bootstrapModalDialog: $('.modal'),
            bootstrapTabs: $(".tabs-custom"),
            bootstrapCollapse: $(".card-custom"),
            rdNavbar: $(".rd-navbar"),
            materialParallax: $(".parallax-container"),
            rdInputLabel: $(".form-label"),
            rdRange: $('.rd-range'),
            wow: $(".wow"),
            owl: $(".owl-carousel"),
            swiper: $(".swiper-slider"),
            statefulButton: $('.btn-stateful'),
            popover: $('[data-toggle="popover"]'),
            viewAnimate: $('.view-animate'),
            radio: $("input[type='radio']"),
            checkbox: $("input[type='checkbox']"),
            counter: $(".counter"),
            progressLinear: $(".progress-linear"),
            progressBar: $(".progress-bar-js"),
            dateCountdown: $('.DateCountdown'),
            lightDynamicGalleryItem: $("[data-lightgallery='dynamic']"),
            inlineToggle: $('.inline-toggle'),
            focusToggle: $('.focus-toggle'),
            countDown: $(".countdown"),
            stepper: $("input[type='number']"),
            radioPanel: $('.radio-panel .radio-inline'),
            slick: $('.slick-slider'),
            videoOverlay: $('.video-overlay'),
            isotope: $(".isotope-wrap")
        };
    $window.on('load', function () {
        if (plugins.isotope.length) {
            for (var i = 0; i < plugins.isotope.length; i++) {
                var
                    wrap = plugins.isotope[i], filterHandler = function (event) {
                        event.preventDefault();
                        for (var n = 0; n < this.isoGroup.filters.length; n++)this.isoGroup.filters[n].classList.remove('active');
                        this.classList.add('active');
                        this.isoGroup.isotope.arrange({filter: this.getAttribute("data-isotope-filter") !== '*' ? '[data-filter*="' + this.getAttribute("data-isotope-filter") + '"]' : '*'});
                    }, resizeHandler = function () {
                        this.isoGroup.isotope.layout();
                    };
                wrap.isoGroup = {};
                wrap.isoGroup.filters = wrap.querySelectorAll('[data-isotope-filter]');
                wrap.isoGroup.node = wrap.querySelector('.isotope');
                wrap.isoGroup.layout = wrap.isoGroup.node.getAttribute('data-isotope-layout') ? wrap.isoGroup.node.getAttribute('data-isotope-layout') : 'masonry';
                wrap.isoGroup.isotope = new Isotope(wrap.isoGroup.node, {
                    itemSelector: '.isotope-item',
                    layoutMode: wrap.isoGroup.layout,
                    filter: '*'
                });
                for (var n = 0; n < wrap.isoGroup.filters.length; n++) {
                    var filter = wrap.isoGroup.filters[n];
                    filter.isoGroup = wrap.isoGroup;
                    filter.addEventListener('click', filterHandler);
                }
                window.addEventListener('resize', resizeHandler.bind(wrap));
            }
        }
        var filterList = $('.isotope-filters-list-link'), filterInfo = $('.isotope-filters-info-text');
        if (filterInfo.length) {
            for (var i = 0; i < filterList.length; i++) {
                var listFilter = $(filterList[i]);
                listFilter.on('click', function () {
                    var itemContent = $(this).find('.isotope-filters-list-text').text() + ' (' + $(this).find('.isotope-filters-list-count').text() + ')';
                    filterInfo.html(itemContent);
                    console.log(true);
                });
            }
        }
    });
    $(function () {
        isNoviBuilder = window.xMode;
        if (plugins.preloader.length && !isNoviBuilder) {
            pageTransition({
                target: document.querySelector('.page'),
                delay: 100,
                duration: preloaderAnimateionDuration,
                classIn: 'fadeIn',
                classOut: 'fadeOut',
                classActive: 'animated',
                conditions: function (event, link) {
                    return !/(\#|callto:|tel:|mailto:|:\/\/)/.test(link) && !event.currentTarget.hasAttribute('data-lightgallery');
                },
                onTransitionStart: function (options) {
                    setTimeout(function () {
                        plugins.preloader.removeClass('loaded');
                    }, options.duration * .75);
                },
                onReady: function () {
                    plugins.preloader.addClass('loaded');
                    windowReady = true;
                }
            });
        }
        function getSwiperHeight(object, attr) {
            var val = object.attr("data-" + attr), dim;
            if (!val) {
                return undefined;
            }
            dim = val.match(/(px)|(%)|(vh)|(vw)$/i);
            if (dim.length) {
                switch (dim[0]) {
                    case "px":
                        return parseFloat(val);
                    case "vh":
                        return $window.height() * (parseFloat(val) / 100);
                    case "vw":
                        return $window.width() * (parseFloat(val) / 100);
                    case "%":
                        return object.width() * (parseFloat(val) / 100);
                }
            } else {
                return undefined;
            }
        }

        function toggleSwiperInnerVideos(swiper) {
            var prevSlide = $(swiper.slides[swiper.previousIndex]), nextSlide = $(swiper.slides[swiper.activeIndex]),
                videos, videoItems = prevSlide.find("video");
            for (var i = 0; i < videoItems.length; i++) {
                videoItems[i].pause();
            }
            videos = nextSlide.find("video");
            if (videos.length) {
                videos.get(0).play();
            }
        }

        function toggleSwiperCaptionAnimation(swiper) {
            var prevSlide = $(swiper.container).find("[data-caption-animate]"),
                nextSlide = $(swiper.slides[swiper.activeIndex]).find("[data-caption-animate]"), delay, duration,
                nextSlideItem, prevSlideItem;
            for (var i = 0; i < prevSlide.length; i++) {
                prevSlideItem = $(prevSlide[i]);
                prevSlideItem.removeClass("animated").removeClass(prevSlideItem.attr("data-caption-animate")).addClass("not-animated");
            }
            var tempFunction = function (nextSlideItem, duration) {
                return function () {
                    nextSlideItem.removeClass("not-animated").addClass(nextSlideItem.attr("data-caption-animate")).addClass("animated");
                    if (duration) {
                        nextSlideItem.css('animation-duration', duration + 'ms');
                    }
                };
            };
            for (var i = 0; i < nextSlide.length; i++) {
                nextSlideItem = $(nextSlide[i]);
                delay = nextSlideItem.attr("data-caption-delay");
                duration = nextSlideItem.attr('data-caption-duration');
                if (!isNoviBuilder) {
                    if (delay) {
                        setTimeout(tempFunction(nextSlideItem, duration), parseInt(delay, 10));
                    } else {
                        setTimeout(tempFunction(nextSlideItem, duration), 0);
                    }
                } else {
                    nextSlideItem.removeClass("not-animated")
                }
            }
        }

        function initOwlCarousel(c) {
            var aliaces = ["-", "-sm-", "-md-", "-lg-", "-xl-", "-xxl-"], values = [0, 576, 768, 992, 1200, 1600],
                responsive = {};
            for (var j = 0; j < values.length; j++) {
                responsive[values[j]] = {};
                for (var k = j; k >= -1; k--) {
                    if (!responsive[values[j]]["items"] && c.attr("data" + aliaces[k] + "items")) {
                        responsive[values[j]]["items"] = k < 0 ? 1 : parseInt(c.attr("data" + aliaces[k] + "items"), 10);
                    }
                    if (!responsive[values[j]]["stagePadding"] && responsive[values[j]]["stagePadding"] !== 0 && c.attr("data" + aliaces[k] + "stage-padding")) {
                        responsive[values[j]]["stagePadding"] = k < 0 ? 0 : parseInt(c.attr("data" + aliaces[k] + "stage-padding"), 10);
                    }
                    if (!responsive[values[j]]["margin"] && responsive[values[j]]["margin"] !== 0 && c.attr("data" + aliaces[k] + "margin")) {
                        responsive[values[j]]["margin"] = k < 0 ? 30 : parseInt(c.attr("data" + aliaces[k] + "margin"), 10);
                    }
                }
            }
            c.on("initialized.owl.carousel", function (event) {
                var $carousel = $(event.currentTarget);
                if (c.attr('data-dots-custom')) {
                    var customPag = $($carousel.attr("data-dots-custom")), active = 0;
                    if ($carousel.attr('data-active')) {
                        active = parseInt($carousel.attr('data-active'), 10);
                    }
                    $carousel.trigger('to.owl.carousel', [active, 300, true]);
                    customPag.find("[data-owl-item='" + active + "']").addClass("active");
                    customPag.find("[data-owl-item]").on('click', function (e) {
                        e.preventDefault();
                        $carousel.trigger('to.owl.carousel', [parseInt(this.getAttribute("data-owl-item"), 10), 300, true]);
                    });
                    $carousel.on("translate.owl.carousel", function (event) {
                        customPag.find(".active").removeClass("active");
                        customPag.find("[data-owl-item='" + event.item.index + "']").addClass("active")
                    });
                }
                if (c.attr('data-nav-custom')) {
                    var customNav = $carousel.parents($carousel.attr("data-nav-custom"));
                    customNav.find(".owl-arrow-next").click(function (e) {
                        e.preventDefault();
                        $carousel.trigger('next.owl.carousel');
                    });
                    customNav.find(".owl-arrow-prev").click(function (e) {
                        e.preventDefault();
                        $carousel.trigger('prev.owl.carousel');
                    });
                }
            });
            c.on("initialized.owl.carousel", function (event) {
            });
            c.owlCarousel({
                autoplay: isNoviBuilder ? false : c.attr("data-autoplay") === "true",
                autoplayTimeout: c.data("autoplay-timeout"),
                autoplayHoverPause: c.data("autoplay-hover-pause"),
                autoplaySpeed: c.data("data-autoplay-speed"),
                center: c.data("data-center"),
                startPosition: c.data("data-start-position"),
                loop: isNoviBuilder ? false : c.attr("data-loop") === "true",
                items: 1,
                rtl: isRtl,
                autoWidth: c.data("data-autowidth") === "true",
                autoHeight: c.data("data-autoheight") === "true",
                dotsContainer: c.attr("data-pagination-class") || false,
                navContainer: c.attr("data-navigation-class") || false,
                mouseDrag: isNoviBuilder ? false : c.attr("data-mouse-drag") !== "false",
                touchDrag: c.data("data-touch-drag"),
                dragEndSpeed: c.data("data-drag-end-speed"),
                nav: c.attr('data-nav') === 'true',
                navSpeed: c.data("data-nav-speed"),
                dots: c.attr("data-dots") === "true",
                dotsSpeed: c.data("dots-speed"),
                dotsEach: c.attr("data-dots-each") ? parseInt(c.attr("data-dots-each"), 10) : false,
                animateIn: c.attr('data-animation-in') ? c.attr('data-animation-in') : false,
                animateOut: c.attr('data-animation-out') ? c.attr('data-animation-out') : false,
                lazyLoad: c.data("data-lazy-load"),
                responsive: responsive,
                navText: function () {
                    try {
                        return JSON.parse(c.attr("data-nav-text"));
                    } catch (e) {
                        return [];
                    }
                }(),
                navClass: function () {
                    try {
                        return JSON.parse(c.attr("data-nav-class"));
                    } catch (e) {
                        return ['owl-prev', 'owl-next'];
                    }
                }()
            });
            var owl = $('.owl-mousewheel');
            owl.on('mousewheel', '.owl-stage', function (e) {
                var curr = $(this);
                if (e.deltaY > 0) {
                    curr.trigger('prev.owl', [800]);
                } else {
                    curr.trigger('next.owl', [800]);
                }
                e.preventDefault();
                e.stopImmediatePropagation();
            });
        }

        function isScrolledIntoView(elem) {
            if (!isNoviBuilder) {
                return elem.offset().top + elem.outerHeight() >= $window.scrollTop() && elem.offset().top <= $window.scrollTop() + $window.height();
            }
            else {
                return true;
            }
        }

        function lazyInit(element, func) {
            $document.on('scroll', function () {
                if ((!element.hasClass('lazy-loaded') && (isScrolledIntoView(element)))) {
                    func.call();
                    element.addClass('lazy-loaded');
                }
            }).trigger("scroll");
        }

        function liveSearch(options) {
            $('#' + options.live).removeClass('cleared').html();
            options.current++;
            options.spin.addClass('loading');

        }

        function initBootstrapTooltip(tooltipPlacement) {
            if (window.innerWidth < 576) {
                plugins.bootstrapTooltip.tooltip('dispose');
                plugins.bootstrapTooltip.tooltip({placement: 'top'});
            } else {
                plugins.bootstrapTooltip.tooltip('dispose');
                plugins.bootstrapTooltip.tooltip({placement: tooltipPlacement});
            }
        }

        if (navigator.platform.match(/(Mac)/i)) {
            $html.addClass("mac-os");
        }
        if (typeof InstallTrigger !== 'undefined') $html.addClass("firefox");
        if (isIE) {
            if (isIE < 10) {
                $html.addClass("lt-ie-10");
            }
            if (isIE < 11) {
                if (plugins.pointerEvents) {
                    $.getScript(plugins.pointerEvents).done(function () {
                        $html.addClass("ie-10");
                        PointerEventsPolyfill.initialize({});
                    });
                }
            }
            if (isIE === 11) {
                $html.addClass("ie-11");
            }
            if (isIE === 12) {
                $html.addClass("ie-edge");
            }
        }
        if (plugins.bootstrapTooltip.length) {
            var tooltipPlacement = plugins.bootstrapTooltip.attr('data-placement');
            initBootstrapTooltip(tooltipPlacement);
            $window.on('resize orientationchange', function () {
                initBootstrapTooltip(tooltipPlacement);
            })
        }
        if (plugins.bootstrapModalDialog.length > 0) {
            for (var i = 0; i < plugins.bootstrapModalDialog.length; i++) {
                var modalItem = $(plugins.bootstrapModalDialog[i]);
                modalItem.on('hidden.bs.modal', $.proxy(function () {
                    var activeModal = $(this), rdVideoInside = activeModal.find('video'),
                        youTubeVideoInside = activeModal.find('iframe');
                    if (rdVideoInside.length) {
                        rdVideoInside[0].pause();
                    }
                    if (youTubeVideoInside.length) {
                        var videoUrl = youTubeVideoInside.attr('src');
                        youTubeVideoInside.attr('src', '').attr('src', videoUrl);
                    }
                }, modalItem))
            }
        }
        if (plugins.popover.length) {
            if (window.innerWidth < 767) {
                plugins.popover.attr('data-placement', 'bottom');
                plugins.popover.popover();
            }
            else {
                plugins.popover.popover();
            }
        }
        if (plugins.statefulButton.length) {
            $(plugins.statefulButton).on('click', function () {
                var statefulButtonLoading = $(this).button('loading');
                setTimeout(function () {
                    statefulButtonLoading.button('reset')
                }, 2000);
            })
        }
        if (plugins.bootstrapTabs.length) {
            for (var i = 0; i < plugins.bootstrapTabs.length; i++) {
                var $bootstrapTabsItem = $(plugins.bootstrapTabs[i]);
                if ($bootstrapTabsItem.attr('data-nav') === 'true') {
                    var $buttonPrev = $($bootstrapTabsItem.find('[data-nav-prev]')).first(),
                        $buttonNext = $($bootstrapTabsItem.find('[data-nav-next]')).first();
                    if ($buttonPrev && $buttonNext) {
                        var isClicked = true, currentIndex = 0, $nav = $($bootstrapTabsItem.find('.nav')),
                            navItemsLength = $nav.children().length;
                        for (var z = 0; z < navItemsLength; z++) {
                            $($nav.find('li:eq(' + z + ') a')).on('hidden.bs.tab', function () {
                                isClicked = true;
                            });
                            $($nav.find('li:eq(' + z + ') a')).on('shown.bs.tab', function () {
                                isClicked = true;
                            });
                        }
                        $buttonPrev.on('click', (function ($nav) {
                            return function () {
                                var prevIndex = $($nav.find('.active')).parent().index() - 1;
                                if ((currentIndex != prevIndex) && prevIndex >= 0 && isClicked) {
                                    currentIndex = prevIndex;
                                    isClicked = false;
                                    $($nav.find('li:eq(' + prevIndex + ') a')).tab('show');
                                }
                            }
                        })($nav));
                        $buttonNext.on('click', (function ($nav) {
                            return function () {
                                var nextIndex = $($nav.find('.active')).parent().index() + 1;
                                if ((currentIndex != nextIndex) && (nextIndex < navItemsLength) && isClicked) {
                                    currentIndex = nextIndex;
                                    isClicked = false;
                                    $($nav.find('li:eq(' + nextIndex + ') a')).tab('show');
                                }
                            }
                        })($nav));
                    }
                }
            }
        }
        if (plugins.bootstrapCollapse.length) {
            for (var i = 0; i < plugins.bootstrapCollapse.length; i++) {
                var $bootstrapCollapseItem = $(plugins.bootstrapCollapse[i]);
                $bootstrapCollapseItem.on('show.bs.collapse', (function ($bootstrapCollapseItem) {
                    return function () {
                        $bootstrapCollapseItem.addClass('active');
                    };
                })($bootstrapCollapseItem));
                $bootstrapCollapseItem.on('hide.bs.collapse', (function ($bootstrapCollapseItem) {
                    return function () {
                        $bootstrapCollapseItem.removeClass('active');
                    };
                })($bootstrapCollapseItem));
            }
        }
        if (plugins.radio.length) {
            for (var i = 0; i < plugins.radio.length; i++) {
                $(plugins.radio[i]).addClass("radio-custom").after("<span class='radio-custom-dummy'></span>")
            }
        }
        if (plugins.checkbox.length) {
            for (var i = 0; i < plugins.checkbox.length; i++) {
                $(plugins.checkbox[i]).addClass("checkbox-custom").after("<span class='checkbox-custom-dummy'></span>")
            }
        }
        if (plugins.owl.length) {
            for (var i = 0; i < plugins.owl.length; i++) {
                var c = $(plugins.owl[i]);
                plugins.owl[i].owl = c;
                initOwlCarousel(c);
            }
        }

        if (plugins.rdNavbar.length) {
            var aliaces, i, j, len, value, values, responsiveNavbar;
            aliaces = ["-", "-sm-", "-md-", "-lg-", "-xl-", "-xxl-"];
            values = [0, 576, 768, 992, 1200, 1600];
            responsiveNavbar = {};
            for (i = j = 0, len = values.length; j < len; i = ++j) {
                value = values[i];
                if (!responsiveNavbar[values[i]]) {
                    responsiveNavbar[values[i]] = {};
                }
                if (plugins.rdNavbar.attr('data' + aliaces[i] + 'layout')) {
                    responsiveNavbar[values[i]].layout = plugins.rdNavbar.attr('data' + aliaces[i] + 'layout');
                }
                if (plugins.rdNavbar.attr('data' + aliaces[i] + 'device-layout')) {
                    responsiveNavbar[values[i]]['deviceLayout'] = plugins.rdNavbar.attr('data' + aliaces[i] + 'device-layout');
                }
                if (plugins.rdNavbar.attr('data' + aliaces[i] + 'hover-on')) {
                    responsiveNavbar[values[i]]['focusOnHover'] = plugins.rdNavbar.attr('data' + aliaces[i] + 'hover-on') === 'true';
                }
                if (plugins.rdNavbar.attr('data' + aliaces[i] + 'auto-height')) {
                    responsiveNavbar[values[i]]['autoHeight'] = plugins.rdNavbar.attr('data' + aliaces[i] + 'auto-height') === 'true';
                }
                if (isNoviBuilder) {
                    responsiveNavbar[values[i]]['stickUp'] = false;
                } else if (plugins.rdNavbar.attr('data' + aliaces[i] + 'stick-up')) {
                    responsiveNavbar[values[i]]['stickUp'] = plugins.rdNavbar.attr('data' + aliaces[i] + 'stick-up') === 'true';
                }
                if (plugins.rdNavbar.attr('data' + aliaces[i] + 'stick-up-offset')) {
                    responsiveNavbar[values[i]]['stickUpOffset'] = plugins.rdNavbar.attr('data' + aliaces[i] + 'stick-up-offset');
                }
            }
            plugins.rdNavbar.RDNavbar({
                anchorNav: !isNoviBuilder,
                stickUpClone: (plugins.rdNavbar.attr("data-stick-up-clone") && !isNoviBuilder) ? plugins.rdNavbar.attr("data-stick-up-clone") === 'true' : false,
                responsive: responsiveNavbar,
                callbacks: {
                    onStuck: function () {
                        var navbarSearch = this.$element.find('.rd-search input');
                        if (navbarSearch) {
                            navbarSearch.val('').trigger('propertychange');
                        }
                        var navbarSelect = plugins.rdNavbar.find('.select2-container');
                        if (navbarSelect.length) {
                            navbarSelect.select2("close");
                        }
                    }, onDropdownOver: function () {
                        return !isNoviBuilder;
                    }, onUnstuck: function () {
                        if (this.$clone === null)
                            return;
                        var navbarSearch = this.$clone.find('.rd-search input');
                        if (navbarSearch) {
                            navbarSearch.val('').trigger('propertychange');
                            navbarSearch.trigger('blur');
                        }
                    }
                }
            });
            if (plugins.rdNavbar.attr("data-body-class")) {
                document.body.className += ' ' + plugins.rdNavbar.attr("data-body-class");
            }
        }
        if (plugins.viewAnimate.length) {
            for (var i = 0; i < plugins.viewAnimate.length; i++) {
                var $view = $(plugins.viewAnimate[i]).not('.active');
                $document.on("scroll", $.proxy(function () {
                    if (isScrolledIntoView(this)) {
                        this.addClass("active");
                    }
                }, $view)).trigger("scroll");
            }
        }
        if (plugins.swiper.length) {
            for (var i = 0; i < plugins.swiper.length; i++) {
                var s = $(plugins.swiper[i]);
                var pag = s.find(".swiper-pagination"), next = s.find(".swiper-button-next"),
                    prev = s.find(".swiper-button-prev"), bar = s.find(".swiper-scrollbar"),
                    swiperSlide = s.find(".swiper-slide"), autoplay = true;
                for (var j = 0; j < swiperSlide.length; j++) {
                    var $this = $(swiperSlide[j]), url;
                    if (url = $this.attr("data-slide-bg")) {
                        $this.css({"background-image": "url(" + url + ")", "background-size": "cover"})
                    }
                }
                swiperSlide.end().find("[data-caption-animate]").addClass("not-animated").end();
                s.swiper({
                    autoplay: s.attr('data-autoplay') ? s.attr('data-autoplay') === "false" || s.attr('data-autoplay-hover') === "true" ? undefined : s.attr('data-autoplay') : 5000,
                    autoplayDisableOnInteraction: false,
                    direction: s.attr('data-direction') ? s.attr('data-direction') : "horizontal",
                    effect: s.attr('data-slide-effect') ? s.attr('data-slide-effect') : "slide",
                    speed: s.attr('data-slide-speed') ? s.attr('data-slide-speed') : 600,
                    keyboardControl: s.attr('data-keyboard') === "true",
                    mousewheelControl: s.attr('data-mousewheel') === "true",
                    mousewheelReleaseOnEdges: s.attr('data-mousewheel-releaase') === "true",
                    lazyLoading: s.attr('data-lazy-loading') === "true",
                    nextButton: next.length ? next.get(0) : null,
                    prevButton: prev.length ? prev.get(0) : null,
                    pagination: pag.length ? pag.get(0) : null,
                    paginationClickable: pag.length ? pag.attr("data-clickable") !== "false" : false,
                    paginationBulletRender: pag.length ? pag.attr("data-index-bullet") === "true" ? function (swiper, index, className) {
                        return '<span class="' + className + '"><span>' + ((index + 1) < 10 ? ('0' + (index + 1)) : (index + 1)) + '</span></span>';
                    } : null : null,
                    scrollbar: bar.length ? bar.get(0) : null,
                    scrollbarDraggable: bar.length ? bar.attr("data-draggable") !== "false" : true,
                    scrollbarHide: bar.length ? bar.attr("data-draggable") === "false" : false,
                    loop: isNoviBuilder ? false : s.attr('data-loop'),
                    simulateTouch: s.attr('data-simulate-touch') && !isNoviBuilder ? s.attr('data-simulate-touch') === "true" : false,
                    onTransitionStart: function (swiper) {
                        toggleSwiperInnerVideos(swiper);
                    },
                    onTransitionEnd: function (swiper) {
                        toggleSwiperCaptionAnimation(swiper);
                    },
                    onInit: function (swiper) {
                        toggleSwiperInnerVideos(swiper);
                        toggleSwiperCaptionAnimation(swiper);
                        if (swiper.container.data('autoplay-hover') === true) {
                            var hoverEvent;
                            swiper.container.mouseenter(function (e) {
                                hoverEvent = setInterval(function () {
                                    swiper.slideNext();
                                }, $(swiper.container).data('autoplay'));
                            });
                            swiper.container.mouseleave(function (e) {
                                clearInterval(hoverEvent);
                            });
                        }
                        // initLightGalleryItem(s.find('[data-lightgallery="item"]'), 'lightGallery-in-carousel');
                    }
                });
                $window.on("resize", (function (s) {
                    return function () {
                        var mh = getSwiperHeight(s, "min-height"), h = getSwiperHeight(s, "height");
                        if (h) {
                            s.css("height", mh ? mh > h ? mh : h : h);
                        }
                    }
                })(s)).trigger("resize");
            }
        }
        if ($html.hasClass("wow-animation") && plugins.wow.length && !isNoviBuilder && isDesktop) {
            new WOW().init();
        }
        if (plugins.rdInputLabel.length) {
            plugins.rdInputLabel.RDInputLabel();
        }

        if (plugins.stepper.length) {
            plugins.stepper.stepper({labels: {up: "", down: ""}});
        }

        if (plugins.counter.length) {
            for (var i = 0; i < plugins.counter.length; i++) {
                var $counterNotAnimated = $(plugins.counter[i]).not('.animated');
                $document.on("scroll", $.proxy(function () {
                    var $this = this;
                    if ((!$this.hasClass("animated")) && (isScrolledIntoView($this))) {
                        $this.countTo({
                            refreshInterval: 40,
                            from: 0,
                            to: parseInt($this.text(), 10),
                            speed: $this.attr("data-speed") || 1000
                        });
                        $this.addClass('animated');
                    }
                }, $counterNotAnimated)).trigger("scroll");
            }
        }
        if (plugins.dateCountdown.length) {
            for (var i = 0; i < plugins.dateCountdown.length; i++) {
                var dateCountdownItem = $(plugins.dateCountdown[i]), time = {
                    "Days": {
                        "text": "Days",
                        "show": true,
                        color: dateCountdownItem.attr("data-color") ? dateCountdownItem.attr("data-color") : "#f9f9f9"
                    },
                    "Hours": {
                        "text": "Hours",
                        "show": true,
                        color: dateCountdownItem.attr("data-color") ? dateCountdownItem.attr("data-color") : "#f9f9f9"
                    },
                    "Minutes": {
                        "text": "Minutes",
                        "show": true,
                        color: dateCountdownItem.attr("data-color") ? dateCountdownItem.attr("data-color") : "#f9f9f9"
                    },
                    "Seconds": {
                        "text": "Seconds",
                        "show": true,
                        color: dateCountdownItem.attr("data-color") ? dateCountdownItem.attr("data-color") : "#f9f9f9"
                    }
                };
                dateCountdownItem.TimeCircles({
                    color: dateCountdownItem.attr("data-color") ? dateCountdownItem.attr("data-color") : "rgba(247, 247, 247, 1)",
                    animation: "smooth",
                    bg_width: dateCountdownItem.attr("data-bg-width") ? dateCountdownItem.attr("data-bg-width") : 0.6,
                    circle_bg_color: dateCountdownItem.attr("data-bg") ? dateCountdownItem.attr("data-bg") : "rgba(0, 0, 0, 1)",
                    fg_width: dateCountdownItem.attr("data-width") ? dateCountdownItem.attr("data-width") : 0.03
                });
                (function (dateCountdownItem, time) {
                    $window.on('load resize orientationchange', function () {
                        if (window.innerWidth < 479) {
                            dateCountdownItem.TimeCircles({
                                time: {
                                    "Days": {
                                        "text": "Days",
                                        "show": true,
                                        color: dateCountdownItem.attr("data-color") ? dateCountdownItem.attr("data-color") : "#f9f9f9"
                                    },
                                    "Hours": {
                                        "text": "Hours",
                                        "show": true,
                                        color: dateCountdownItem.attr("data-color") ? dateCountdownItem.attr("data-color") : "#f9f9f9"
                                    },
                                    "Minutes": {
                                        "text": "Minutes",
                                        "show": true,
                                        color: dateCountdownItem.attr("data-color") ? dateCountdownItem.attr("data-color") : "#f9f9f9"
                                    },
                                    Seconds: {
                                        "text": "Seconds",
                                        show: false,
                                        color: dateCountdownItem.attr("data-color") ? dateCountdownItem.attr("data-color") : "#f9f9f9"
                                    }
                                }
                            }).rebuild();
                        } else if (window.innerWidth < 767) {
                            dateCountdownItem.TimeCircles({
                                time: {
                                    "Days": {
                                        "text": "Days",
                                        "show": true,
                                        color: dateCountdownItem.attr("data-color") ? dateCountdownItem.attr("data-color") : "#f9f9f9"
                                    },
                                    "Hours": {
                                        "text": "Hours",
                                        "show": true,
                                        color: dateCountdownItem.attr("data-color") ? dateCountdownItem.attr("data-color") : "#f9f9f9"
                                    },
                                    "Minutes": {
                                        "text": "Minutes",
                                        "show": true,
                                        color: dateCountdownItem.attr("data-color") ? dateCountdownItem.attr("data-color") : "#f9f9f9"
                                    },
                                    Seconds: {
                                        text: '',
                                        show: false,
                                        color: dateCountdownItem.attr("data-color") ? dateCountdownItem.attr("data-color") : "#f9f9f9"
                                    }
                                }
                            }).rebuild();
                        } else {
                            dateCountdownItem.TimeCircles({time: time}).rebuild();
                        }
                    });
                    $window.trigger('resize');
                })(dateCountdownItem, time);
            }
        }
        if (plugins.progressBar.length) {
            var i, bar, type;
            for (i = 0; i < plugins.progressBar.length; i++) {
                var progressItem = plugins.progressBar[i];
                bar = null;
                if (progressItem.className.indexOf("progress-bar-horizontal") > -1) {
                    type = 'Line';
                }
                if (progressItem.className.indexOf("progress-bar-radial") > -1) {
                    type = 'Circle';
                }
                if (progressItem.getAttribute("data-stroke") && progressItem.getAttribute("data-value") && type) {
                    bar = new ProgressBar[type](progressItem, {
                        strokeWidth: Math.round(parseFloat(progressItem.getAttribute("data-stroke")) / progressItem.offsetWidth * 100),
                        trailWidth: progressItem.getAttribute("data-trail") ? Math.round(parseFloat(progressItem.getAttribute("data-trail")) / progressItem.offsetWidth * 100) : 0,
                        text: {
                            value: progressItem.getAttribute("data-counter") === "true" ? '0' : null,
                            className: 'progress-bar__body',
                            style: null
                        }
                    });
                    bar.svg.setAttribute('preserveAspectRatio', "none meet");
                    if (type === 'Line') {
                        bar.svg.setAttributeNS(null, "height", progressItem.getAttribute("data-stroke"));
                    }
                    bar.path.removeAttribute("stroke");
                    bar.path.className.baseVal = "progress-bar__stroke";
                    if (bar.trail) {
                        bar.trail.removeAttribute("stroke");
                        bar.trail.className.baseVal = "progress-bar__trail";
                    }
                    if (progressItem.getAttribute("data-easing") && !isIE) {
                        $document.on("scroll", {"barItem": bar}, $.proxy(function (event) {
                            var bar = event.data.barItem;
                            var $this = $(this);
                            if (isScrolledIntoView($this) && this.className.indexOf("progress-bar--animated") === -1) {
                                this.className += " progress-bar--animated";
                                bar.animate(parseInt($this.attr("data-value"), 10) / 100.0, {
                                    easing: $this.attr("data-easing"),
                                    duration: $this.attr("data-duration") ? parseInt($this.attr("data-duration", 10), 10) : 800,
                                    step: function (state, b) {
                                        if (b._container.className.indexOf("progress-bar-horizontal") > -1 || b._container.className.indexOf("progress-bar-vertical") > -1) {
                                            b.text.style.width = Math.abs(b.value() * 100).toFixed(0) + "%"
                                        }
                                        b.setText(Math.abs(b.value() * 100).toFixed(0));
                                    }
                                });
                            }
                        }, progressItem)).trigger("scroll");
                    } else {
                        bar.set(parseInt($(progressItem).attr("data-value"), 10) / 100.0);
                        bar.setText($(progressItem).attr("data-value"));
                        if (type === 'Line') {
                            bar.text.style.width = parseInt($(progressItem).attr("data-value"), 10) + "%";
                        }
                    }
                } else {
                    console.error(progressItem.className + ": progress bar type is not defined");
                }
            }
        }
        if (plugins.progressLinear.length) {
            for (i = 0; i < plugins.progressLinear.length; i++) {
                var progressBar = $(plugins.progressLinear[i]);
                $window.on("scroll load", $.proxy(function () {
                    var bar = $(this);
                    if (!bar.hasClass('animated-first') && isScrolledIntoView(bar)) {
                        var end = parseInt($(this).find('.progress-value').text(), 10);
                        bar.find('.progress-bar-linear').css({width: end + '%'});
                        bar.find('.progress-value').countTo({refreshInterval: 40, from: 0, to: end, speed: 500});
                        bar.addClass('animated-first');
                    }
                }, progressBar));
            }
        }
        if (plugins.materialParallax.length) {
            if (!isNoviBuilder && !isIE && !isMobile) {
                plugins.materialParallax.parallax();
                $window.on('load', function () {
                    setTimeout(function () {
                        $window.scroll();
                    }, 500);
                });
            } else {
                for (var i = 0; i < plugins.materialParallax.length; i++) {
                    var parallax = $(plugins.materialParallax[i]), imgPath = parallax.data("parallax-img");
                    parallax.css({"background-image": 'url(' + imgPath + ')', "background-size": "cover"});
                }
            }
        }
        if (plugins.rdRange.length && !isNoviBuilder) {
            plugins.rdRange.RDRange({});
        }
        if (plugins.inlineToggle.length) {
            for (var i = 0; i < plugins.inlineToggle.length; i++) {
                var $element = $(plugins.inlineToggle[i]);
                $element.on('click', (function ($element) {
                    return function (event) {
                        event.preventDefault();
                        $element.parents(".inline-toggle-parent").toggleClass("active");
                    }
                })($element));
                $body.on('click', $element, (function ($element) {
                    return function (event) {
                        if (event.target !== event.data[0] && !$(event.target).hasClass("inline-toggle-parent") && event.data.find($(event.target)).length === 0) {
                            $element.parents(".inline-toggle-parent").removeClass("active");
                        }
                    }
                })($element));
            }
        }
        if (plugins.focusToggle.length) {
            for (var i = 0; i < plugins.focusToggle.length; i++) {
                var $element = $(plugins.focusToggle[i]);
                $element.hover(function (event) {
                    event.preventDefault();
                    $(this).parents('.focus-toggle-parent').addClass('focus');
                });
                $element.parents('.focus-toggle-parent').hover(function () {
                }, function () {
                    $(this).removeClass('focus');
                })
            }
        }
        if (plugins.countDown.length) {
            for (var i = 0; i < plugins.countDown.length; i++) {
                var $countDownItem = $(plugins.countDown[i]), d = new Date(), type = $countDownItem.attr('data-type'),
                    time = $countDownItem.attr('data-time'), format = $countDownItem.attr('data-format'), settings = [];
                if ($countDownItem.attr('data-style') === 'short') {
                    settings['labels'] = ['Yeas', 'Mons', 'Weks', 'Days', 'Hrs', 'Mins', 'Secs'];
                }
                d.setTime(Date.parse(time)).toLocaleString();
                settings[type] = d;
                settings['format'] = format;
                $countDownItem.countdown(settings);
            }
        }
        if (plugins.radioPanel) {
            for (var i = 0; i < plugins.radioPanel.length; i++) {
                var $element = $(plugins.radioPanel[i]);
                $element.on('click', function () {
                    plugins.radioPanel.removeClass('active');
                    $(this).addClass('active');
                })
            }
        }
        if (plugins.slick.length) {
            for (var i = 0; i < plugins.slick.length; i++) {
                var $slickItem = $(plugins.slick[i]);
                $slickItem.on('init', function (slick) {
                    // initLightGallery($(slick).find('[data-lightgallery="item"]'), 'lightGallery-in-carousel');
                });
                $slickItem.slick({
                    slidesToScroll: parseInt($slickItem.attr('data-slide-to-scroll'), 10) || 1,
                    asNavFor: $slickItem.attr('data-for') || false,
                    dots: $slickItem.attr("data-dots") === "true",
                    infinite: isNoviBuilder ? false : $slickItem.attr("data-loop") === "true",
                    focusOnSelect: true,
                    arrows: $slickItem.attr("data-arrows") === "true",
                    swipe: $slickItem.attr("data-swipe") === "true",
                    autoplay: isNoviBuilder ? false : $slickItem.attr("data-autoplay") === "true",
                    autoplaySpeed: $slickItem.attr("data-autoplay-speed") ? parseInt($slickItem.attr("data-autoplay-speed")) : 3500,
                    vertical: $slickItem.attr("data-vertical") === "true",
                    centerMode: $slickItem.attr("data-center-mode") === "true",
                    centerPadding: $slickItem.attr("data-center-padding") ? $slickItem.attr("data-center-padding") : '0.50',
                    mobileFirst: true,
                    rtl: isRtl,
                    responsive: [{
                        breakpoint: 0,
                        settings: {slidesToShow: parseInt($slickItem.attr('data-items'), 10) || 1}
                    }, {
                        breakpoint: 575,
                        settings: {slidesToShow: parseInt($slickItem.attr('data-sm-items'), 10) || 1}
                    }, {
                        breakpoint: 767,
                        settings: {slidesToShow: parseInt($slickItem.attr('data-md-items'), 10) || 1}
                    }, {
                        breakpoint: 991,
                        settings: {slidesToShow: parseInt($slickItem.attr('data-lg-items'), 10) || 1}
                    }, {
                        breakpoint: 1199,
                        settings: {slidesToShow: parseInt($slickItem.attr('data-xl-items'), 10) || 1}
                    }]
                }).on('afterChange', function (event, slick, currentSlide, nextSlide) {
                    var $this = $(this), childCarousel = $this.attr('data-child');
                    if (childCarousel) {
                        $(childCarousel + ' .slick-slide').removeClass('slick-current');
                        $(childCarousel + ' .slick-slide').eq(currentSlide).addClass('slick-current');
                    }
                });
            }
        }
        if (plugins.videoOverlay.length) {
            for (var i = 0; i < plugins.videoOverlay.length; i++) {
                var overlay = plugins.videoOverlay[i];
                if (overlay) {
                    overlay.style.opacity = '1';
                    overlay.addEventListener('click', function (e) {
                        $(this).animate({opacity: 0}, function () {
                            this.style.display = 'none';
                        });
                    });
                }
            }
        }
        function getRandomInt(min, max) {
            return Math.floor(Math.random() * (max - min + 1)) + min;
        }

    });
}());