define(['Backbone', 'marionette', 'jquery', 'underscore', 'app/core/mediator', 'text!app/views/pagination.tpl'], function(Backbone, Marionette, $, _, mediator, template) {

    var PaginationView = Marionette.Layout.extend({
        tagName: 'div',
        className: 'paginationView',
        template: _.template(template),
        initialize: function(options) {
            this.collection = options.collection;
        },
        events: {
            'click .nextPage': 'goNext',
            'click .prevPage': 'goPrev',
            'click .pageNumber': 'clickPage'
        },
        serializeData: function() {
            var that = this;
            return {
                'totalPages': that.collection.totalPages,
                'totalResults': that.collection.totalResults,
                'hasNext': function() {
                    if ((that.collection.currentPage === that.collection.totalPages) || that.collection.totalPages === 0) {
                        return false;
                    } 
                    return true;
                },
                'hasPrev': function() {
                    if (that.collection.currentPage <= 1) {
                        return false;
                    }
                    return true;
                },

                //returns the page numbers to show in the paginator view - first page, last page, current page, and pages before and after current page. FIXME: does this make sense?
                'pagesToShow': function() {
                    var pages = [];
                    var currentPage = that.collection.currentPage;
                    var totalPages = that.collection.totalPages;
                    if (totalPages === 0) {
                        return [];
                    }

                    var pageMax = totalPages - currentPage < 9 ? totalPages : currentPage + 9;
                    for (var i=currentPage; i <= pageMax; i++) {
                        pages.push(i);
                    }

                    var pageMin = currentPage - 0 < 9 ? 0 : currentPage - 9;
                    for (var j=currentPage; j > pageMin; j--) {
                        pages.push(j);
                    }

                    /*
                    pages.push(1);
                    pages.push(currentPage);
                    pages.push(totalPages);
                    if (currentPage !== 1) {
                        pages.push(currentPage - 1);
                    }
                    if (currentPage !== totalPages) {
                        pages.push(currentPage + 1);
                    }
                    */
                    return _.uniq(pages).sort(function(a, b) {
                        return parseInt(a) - parseInt(b);
                    });
                }

            }
        },

        goNext: function() {
            this.gotoPage(this.collection.currentPage + 1);
        },

        goPrev: function() {
            this.gotoPage(this.collection.currentPage - 1);
        },
        gotoPage: function(page) {
            mediator.commands.execute("search:setPage", page);
            mediator.commands.execute("search:submit");
        },
        clickPage: function(e) {
            var $elem = $(e.target);
            var page = parseInt($elem.text());
            this.gotoPage(page);
        },
        onRender: function() {
            this.$el.addClass('smallFont');
            var currentPage = this.collection.currentPage;
            this.$el.find('.pageNumber').each(function() {
                var page = parseInt($(this).text());
                if (page === currentPage) {
                    $(this).addClass('paginationSelected');
                }
            });
        }
         

    });

    return PaginationView;
});
