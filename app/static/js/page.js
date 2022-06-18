function Pager(settings) {
    var extend = function (tgt, src) {
        for (var p in src)
            tgt[p] = src[p];
        return tgt;
    }
    var cfg = extend({
        size: 1,                                //页数
        current: 0,                            //当前页码
        beforeEnd: 2,                        //首尾最少显示页数
        visible: 5,                            //中间可见页数
        prevLabel: '上一页',
        nextLabel: '下一页',
        ellipsis: '<span></span>',    //省略标记
        textboxEnabled: true,            //是否显示文本域
        showAlways: false                //总是显示分页器
    }, settings || {});

    if (!cfg.showAlways && cfg.size == 1)
        return false;

    var prev = (cfg.size == 1 || cfg.current == 0) ?
    '<span class="prev">' + cfg.prevLabel + '</span>' :
        //'<a href="'+cfg.prefix+(cfg.current==1?'':'_'+(cfg.current-1))+'.'+cfg.suffix+'" class="prev">'+cfg.prevLabel+'</a>';
        //'<a href="?searchtype=1&page_index=0&buyerName=&projectId=&dbselect=bidx&kw=%E5%8C%97%E4%BA%AC&start_time=2017%3A03%3A30&end_time=2017%3A04%3A06&timeType=2&bidSort=0&pinMu=0&bidType=0&displayZone=&zoneId=&agentName='+'" class="prev">'+cfg.prevLabel+'</a>';
    '<a href="javascript:void(0)" onclick="gopage('+(page_index-1)+')" class="prev">' + cfg.prevLabel + '</a>';
    var next = (cfg.size == cfg.current + 1) ?
    '<span class="next">' + cfg.nextLabel + '</span>' :
        //'<a href="?searchtype=1&page_index=2&buyerName=&projectId=&dbselect=infox&kw=%E5%8C%97%E4%BA%AC&start_time=2017%3A03%3A30&end_time=2017%3A04%3A06&timeType=2&bidSort=0&pinMu=0&bidType=0&displayZone=&zoneId=&agentName='+'" class="next">'+cfg.nextLabel+'</a>';
    '<a href="javascript:void(0)" onclick="gopage('+(page_index+1)+')" class="next">' + cfg.nextLabel + '</a>';
    var first = (cfg.current == 0) ?
        '<span class="current">1</span>' :
    '<a href="javascript:void(0)" onclick="gopage(1)">' + '1</a>';

    var p = function (s) {
        document.write(s);
    }

    p(prev);
    p(first);

    if (cfg.size > 1) {
        var generator = function (begin, end) {
            for (var i = begin; i < end; i++) {
                cfg.current == i ?
                    p('<span class="current">' + (i + 1) + '</span>') :
                    //p('<a href="?searchtype=1&page_index='+(i+1)+'&dbselect=infox&kw=%E5%8C%97%E4%BA%AC&buyerName=&projectId=&start_time=2017%3A03%3A30&end_time=2017%3A04%3A06&timeType=2&bidSort=0&pinMu=0&bidType=0&displayZone=&zoneId=&agentName='+'">'+(i+1)+'</a>');
                    p('<a href="javascript:void(0)" onclick="gopage(' + (i + 1) + ')">' + (i + 1) + '</a>');

            }
        }

        //visible定义区间计算
        var posBegin = Math.max(0, cfg.current - (cfg.visible - Math.ceil(cfg.visible / 2)));
        var posEnd = Math.min(posBegin + cfg.visible, cfg.size);
        //头部
        generator(1, Math.min(cfg.beforeEnd, cfg.size));
        //中间
        if (cfg.current >= posBegin) {
            if (cfg.beforeEnd < posBegin)        p(cfg.ellipsis);
            generator(Math.max(posBegin, cfg.beforeEnd), posEnd);
        }
        //尾部
        if (posEnd != cfg.size) {
            if (cfg.size - cfg.beforeEnd > posEnd)        p(cfg.ellipsis);
            generator(Math.max(cfg.size - cfg.beforeEnd, posEnd), cfg.size);
        }
    }
    p(next);


}


function gopage(e) {
    $("#page_index").val(e);
    validateCode();
}
function loadimage() {
    document.getElementById("randImage").src = basePath + "ValidateImage?" + Math.random();
}