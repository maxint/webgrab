/*
 * common.js
 * Copyright (C) 2014 maxint <NOT_SPAM_lnychina@gmail.com>
 *
 * Distributed under terms of the MIT license.
 */


function withjQuery(callback, safe) {
    if (typeof(jQuery) == "undefined") {
        var script = document.createElement("script");
        script.type = "text/javascript";
        script.src = "https://ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js";
        if (safe) {
            var cb = document.createElement("script");
            cb.type = "text/javascript";
            cb.textContent = "jQuery.noConflict();(" + callback.toString() + ")(jQuery, window);";
            script.addEventListener('load', function(){
                document.head.appendChild(cb);
            });
        } else {
            var dollar = undefined;
            if (typeof($) != "undefined") dollar = $;
            script.addEventListener('load', function(){
                jQuery.noConflict();
                $ = dollar;
                callback(jQuery, window);
            });
        }
        document.head.appendChild(script);
    } else {
        console.log('Using jquery ' + jQuery().jquery);
        $(document).ready(function(){
            console.log('Runing custom script');
            callback(jQuery, typeof(unsafeWindow) == "undefined" ? window : unsafeWindow);
        });
    }
}

function getParameterByName(name) {
    name = name.replace(/[\[]/, "\\[").replace(/[\]]/, "\\]");
    var regex = new RegExp("[\\?&]" + name + "=([^&#]*)"),
        results = regex.exec(location.search);
    return results === null ? null : decodeURIComponent(results[1].replace(/\+/g, " "));
}

function basename(path) {
    return path.replace(/\\/g,'/').replace( /.*\//, '' );
}

function dirname(path) {
    return path.replace(/\\/g,'/').replace(/\/[^\/]*$/, '');;
}

// the guts of this userscript
withjQuery(function($, window){
    // "back to top" button
    $('#backtop').click(function(){
        document.documentElement.scrollTop = 0;
        window.onscroll();
    });
    window.onscroll = function (){
        if (document.documentElement.scrollTop == 0)
            $('#backtop').hide();
        else
            $('#backtop').show();
    };
    var category = getParameterByName('category');
    var id = getParameterByName('id');
    //var root = window.location.origin + dirname(window.location.pathname);
    if (category == null)
        category = 'Marketing';
    if (category == 'Marketing' || category == 'Technology' || category == 'Algorithm') {
        $('#header-image').attr('src', 'images/' + category + '.jpg');
        if (id == null) {
            // list page
            $.get(category + '.html', function(data){
                data = $(data);
                $('#main').empty().append(data.find('#main').html());
                document.title = data.find('title').text();
                // generate list
                $.getJSON('mag.json', function(mag) {
                    $("ol[id^='M_']").each(function(){
                        var cat = $(this).attr('id').substr(2);
                        var range = mag.categories[cat];
                        if (range) {
                            $(this).empty().each(function(){
                                for (var i = range.start; i < range.end; ++i) {
                                    var post = mag.posts[i];
                                    $('<li><a href="?category=' + category + '&id=' + i + '">' + post.title +'</a></li>').appendTo($(this));
                                }
                            });
                        } else {
                            console.log('Can not find "' + cat + '" in mag.json');
                        }
                    });
                });
            });
        } else {
            // post
            $.getJSON('mag.json', function(mag) {
                var count = mag.posts.length;
                var id0 = parseInt(id);
                id = Math.min(count-1, Math.max(0, id0));
                $.get('post.html', function(data){
                    var post = mag.posts[id];
                    data = $(data);
                    data.find('#title').html(post.title);
                    data.find('#original_url').attr('href', post.url);
                    data.find('#date').first().each(function(){
                        var html = $(this).html();
                        var year = Math.floor(post.date / 10000);
                        var month = Math.floor((post.date % 10000) / 100);
                        var day = Math.floor(post.date % 100);
                        html = html.replace('${year}', year).replace('${month}', month).replace('${day}', day);
                        $(this).html(html);
                    });
                    data.find('#nav_prev a').attr('href', '?category=' + category + '&id=' + (id - 1 + count) % count);
                    data.find('#nav_next a').attr('href', '?category=' + category + '&id=' + (id + 1) % count);
                    $('#main').empty().append(data.find('#main').html());
                    $('#content').load('posts/' + id + '.html');
                    document.title = post.title;
                });
            });
        }
    }
}, true)
