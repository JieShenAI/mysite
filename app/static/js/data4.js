function GetTwoDigit(arr) {
    var v = arr;
    if (v > 9)return v.toString();
    return "0" + v;
}

function showdate(n) {
    var uom = new Date(new Date() - 0 + n * 86400000);
    uom = uom.getFullYear() + ":" + GetTwoDigit(uom.getMonth() + 1) + ":" + GetTwoDigit(uom.getDate());
    return uom;
}
function delHtmlTag(str)
{
return str.replace(/<[^>]+>/g,"");//去掉所有的html标记
}
function dosearch(e) {
if(e!==1 && e!==2){
e=$("#searchtype").val();
}
if(e=="" || e=="undefined"){e=1}
$("#searchtype").val(e);
$("#buyerName").val($("#inpBuyerName").val());
$("#projectId").val($("#inpProjectId").val());
$("#agentName").val($("#inpAgentName").val());
var value1 = $("#inpCusStartTime").val();
    var value2 = $("#inpCusEndTime").val();
$("#start_time").val(value1.replace(/-/g, ":"));
$("#end_time").val(value2.replace(/-/g, ":"));


if (cusStatus==1 || dateTy == '6'){
    var value1 = $("#inpCusStartTime").val();
    var value2 = $("#inpCusEndTime").val();
    $("#start_time").val(value1.replace(/-/g, ":"));
    $("#end_time").val(value2.replace(/-/g, ":"));
    if (value1 == "" || value2 == "") {
        alert("请选择要查询的日期或选择其他时间选项！");
        return false;
    } else {
        $("#timeType").val("6");
        var value1 = $("#inpCusStartTime").val();
        var value2 = $("#inpCusEndTime").val();
        $("#start_time").val(value1.replace(/-/g, ":"));
        $("#end_time").val(value2.replace(/-/g, ":"));

        document.searchForm.submit();
    }

}else{

    document.searchForm.submit();
}



}

$("document").ready(function () {
    $("#uniqid").val("99901");
    $("span[class='inf']").click(function () {
        window.location.href = "oldsearch?searchtype=1&page_index=1&bidSort=0&buyerName=&projectId=&pinMu=0&bidType=0&dbselect=bidx&kw=&start_time=&end_time=&timeType=1&displayZone=&zoneId=&agentName=";
    });
    //zone点击
    $("#inpDisplayZone").mouseover(function () {
        $(this).css("cursor", "pointer");
    });
    $("#inpDisplayZone").focus(function () {
        $(this).css("cursor", "pointer");
        $(".zone_list_container").show();
    });
    $(".zone_list > li").mouseover(function () {
        $(this).css({"background": "#0082d4", "color": "#fff", "cursor": "pointer"});
    });
    $(".zone_list > li").mouseout(function () {
        $(this).css({"background": "#fff", "color": "#777"});
    });
    $(".zone_list > li").click(function () {
        var st = $(this).attr("zoneId");
        var st2 = $(this).text();
        $("#zoneId").val(st);
        $("#displayZone").val(st2);
        $(".zone_list_container").hide();
        $("#inpDisplayZone").val(st2);
        $("#inpZoneId").val(st);
        //doit
        $("#buyerName").val($("#inpBuyerName").val());
        $("#projectId").val($("#inpProjectId").val());
        $("#agentName").val($("#inpAgentName").val());
        //doit
        validateCode();
        //document.searchForm.submit();
    });

    //zone点击结束

    //cusTime开始
    $(".cusTime_container").hide();
    $("#cusTime").click(function () {
        $("#datesel > li").hide();
        $(".cusTime_container").show();
    });
    $(".cusTime_container em.clos").click(function () {
        $(".cusTime_container").hide();
        $("#datesel > li").show();
    });
    /*
    $("#inpCusStartTime").click(function () {
        if (self.gfPop)gfPop.fPopCalendar(document.getElementById("inpCusStartTime"));
        return false;
    });
    $("#inpCusEndTime").click(function () {
        if (self.gfPop)gfPop.fPopCalendar(document.getElementById("inpCusEndTime"));
        return false;
    });
    */
    $(".cusTime_container em.dose").click(function () {//先转换格式，后提交表格
        var value1 = $("#inpCusStartTime").val();
        var value2 = $("#inpCusEndTime").val();
        if (value1 == "" || value2 == "") {
            alert("请选择要查询的日期或选择其他时间选项！");
            return false;
        } else {
            $("#start_time").val(value1.replace(/-/g, ":"));
            $("#end_time").val(value2.replace(/-/g, ":"));
            $("#timeType").val("6");
            //doit
            $("#buyerName").val($("#inpBuyerName").val());
            $("#projectId").val($("#inpProjectId").val());
            $("#agentName").val($("#inpAgentName").val());
            //doit
            validateCode();
            //document.searchForm.submit();
        }
    });
    //cusTime结束

    $("#datesel li").each(function () {
        $(this).css("background", "#fff");
    });

    $("#datesel li").eq(dateTy).css({"background": "#0082d4", "color": "#fff"});

    $("#datesel li").not(":eq("+dateTy+")").mouseover(function () {
        $(this).css({"background": "#8a8a8a", "color": "#fff", "cursor": "pointer"});
    });
    $("#datesel li").not(":eq("+dateTy+")").mouseout(function () {
        $(this).css({"background": "#fff", "color": "#555"});
    });
    if (dateTy == '6') {
        $("#datesel > li").hide();
        $(".cusTime_container").show();
    }


    $("#searchbidTypeSel li").each(function () {
        $(this).css("background", "#fff");
    });

    $("#searchbidTypeSel li").eq(bidType).css({"background": "#0082d4", "color": "#fff"});


    $("#searchbidTypeSel li").not(":eq("+bidType+")").mouseover(function () {
        $(this).css({"background": "#8a8a8a", "color": "#fff", "cursor": "pointer"});
    });
    $("#searchbidTypeSel li").not(":eq("+bidType+")").mouseout(function () {
        $(this).css({"background": "#fff", "color": "#555"});
    });
    $("#searchbidTypeSel li:last").mouseover(function () {
        $(this).css({"background": "#fff", "color": "#fff", "cursor": "pointer"});
    });
    $("#searchbidTypeSel li:last").mouseout(function () {
        $(this).css({"background": "#fff", "color": "#fff", "cursor": "pointer"});
    });


    $("#searchBidSortSel li").each(function () {
        $(this).css("background", "#fff");
    });

    $("#searchBidSortSel li").eq(bidSort).css({"background": "#0082d4", "color": "#fff"});

    $("#searchBidSortSel li").not(":eq("+bidSort+")").mouseover(function () {
        $(this).css({"background": "#8a8a8a", "color": "#fff", "cursor": "pointer"});
    });
    $("#searchBidSortSel li").not(":eq("+bidSort+")").mouseout(function () {
        $(this).css({"background": "#fff", "color": "#555"});
    });

    $("#searchPinMuSel li").each(function () {
        $(this).css("background", "#fff");
    });

    $("#searchPinMuSel li").eq(pinMu).css({"background": "#0082d4", "color": "#fff"});

    $("#searchPinMuSel li").not(":eq("+pinMu+")").mouseover(function () {
        $(this).css({"background": "#8a8a8a", "color": "#fff", "cursor": "pointer"});
    });
    $("#searchPinMuSel li").not(":eq("+pinMu+")").mouseout(function () {
        $(this).css({"background": "#fff", "color": "#555"});
    });


    if ($("#vT_bidSearch_o").css("display") == "none") {
        $(".vT-srch-result-channel-con").css("margin-top", "0")
    }

    // $(".vT_search_sortby li:not(.current)").mouseover(function () {
    //     $(this).css("background", "#d0d0d0");
    //     $(this).css("text-decoration", "underline");
    // });
    // $(".vT_search_sortby li:not(.current)").mouseout(function () {
    //     $(this).css("background", "#ececec");
    //     $(this).css("text-decoration", "none");
    // });

     $(".vT_search_sortby li:not(.current2)").mouseover(function () {
        $(this).css("background", "#d0d0d0");
        $(this).css("text-decoration", "underline");
    });
    $(".vT_search_sortby li:not(.current2)").mouseout(function () {
        $(this).css("background", "#ececec");
        $(this).css("text-decoration", "none");
    });

    $('#kw').bind('blur',function(event){
        $(this).val(delHtmlTag($(this).val()));
    });
    $('#inpBuyerName').bind('blur',function(event){
        $(this).val(delHtmlTag($(this).val()));
    });
    $('#inpProjectId').bind('blur',function(event){
        $(this).val(delHtmlTag($(this).val()));
    });
    $('#inpAgentName').bind('blur',function(event){
        $(this).val(delHtmlTag($(this).val()));
    });

    $('#kw').bind('keypress', function (event) {
        $(this).val(delHtmlTag($(this).val()));
        if (event.keyCode == "13") {
            $("#buyerName").val($("#inpBuyerName").val());
            $("#projectId").val($("#inpProjectId").val());
            $("#agentName").val($("#inpAgentName").val());
            validateCode();
            return;
        }
    });

    $('#inpid').bind('keypress', function (event) {
        if (event.keyCode == "13") {
            $("#buyerName").val($("#inpBuyerName").val());
            $("#projectId").val($("#inpProjectId").val());
            $("#agentName").val($("#inpAgentName").val());
            validateCode();
            return;
        }
    });

    $('#inpBuyerName').bind('keypress', function (event) {
        $(this).val(delHtmlTag($(this).val()));
        if (event.keyCode == "13") {
            $("#buyerName").val($("#inpBuyerName").val());
            $("#projectId").val($("#inpProjectId").val());
            $("#agentName").val($("#inpAgentName").val());
            validateCode();
        }
    });

    $('#inpProjectId').bind('keypress', function (event) {
        $(this).val(delHtmlTag($(this).val()));
        if (event.keyCode == "13") {
            $("#buyerName").val($("#inpBuyerName").val());
            $("#projectId").val($("#inpProjectId").val());
            $("#agentName").val($("#inpAgentName").val());
            validateCode();
        }
    });

    $('#inpAgentName').bind('keypress', function (event) {
        $(this).val(delHtmlTag($(this).val()));
        if (event.keyCode == "13") {
            $("#buyerName").val($("#inpBuyerName").val());
            $("#projectId").val($("#inpProjectId").val());
            $("#agentName").val($("#inpAgentName").val());
            validateCode();
        }
    });

    //ppp开始
    if ($("#pppStatus").val() == "1") {
        $("#disPPP").attr("src", staticPath + "images/ppp_on.gif");
    } else {
        $("#disPPP").attr("src", staticPath + "images/ppp_off.gif");
    }
    //ppp结束

});
function timeSel(e) {
    var myDate = new Date();
    var currentDate = myDate.getFullYear() + ":" + GetTwoDigit(myDate.getMonth() + 1) + ":" + GetTwoDigit(myDate.getDate());
    var time0 = currentDate;//今天
    var time3d = showdate(-3);//近3日
    var time1w = showdate(-7);//近1周
    var time1m = showdate(-31);//近1月
    var time3m = showdate(-92);//近3月
    var time6m = showdate(-182);//近半年

    if (e == 0) {
        $("#start_time").val(time0);
        $("#end_time").val(time0);
        $("#inpCusStartTime").val(time0);
        $("#inpCusEndTime").val(time0);
    }
    if (e == 1) {
        $("#start_time").val(time3d);
        $("#end_time").val(time0);
        $("#inpCusStartTime").val(time3d);
        $("#inpCusEndTime").val(time0);
    }
    if (e == 2) {
        $("#start_time").val(time1w);
        $("#end_time").val(time0);
        $("#inpCusStartTime").val(time1w);
        $("#inpCusEndTime").val(time0);
    }
    if (e == 3) {
        $("#start_time").val(time1m);
        $("#end_time").val(time0);
        $("#inpCusStartTime").val(time1m);
        $("#inpCusEndTime").val(time0);
    }
    if (e == 4) {
        $("#start_time").val(time3m);
        $("#end_time").val(time0);
        $("#inpCusStartTime").val(time3m);
        $("#inpCusEndTime").val(time0);
    }
    if (e == 5) {
        $("#start_time").val(time6m);
        $("#end_time").val(time0);
        $("#inpCusStartTime").val(time6m);
        $("#inpCusEndTime").val(time0);
    }
    $("#timeType").val(e);
    dateTy=e;
    //doit
    $("#buyerName").val($("#inpBuyerName").val());
    $("#projectId").val($("#inpProjectId").val());
    $("#agentName").val($("#inpAgentName").val());
    //doit
    validateCode();
    //document.searchForm.submit();
}
function bidTypeSel(e) {
    $("#bidType").val(e);
    //doit
    $("#buyerName").val($("#inpBuyerName").val());
    $("#projectId").val($("#inpProjectId").val());
    $("#agentName").val($("#inpAgentName").val());
    //doit
    validateCode();
    //document.searchForm.submit();
}
function isPPP() {
    var ppps = $("#pppStatus").val();
    if (ppps == 1) {
        $("#pppStatus").val("")
    } else {
        $("#pppStatus").val("1")
    }
    //doit
    validateCode();
    //document.searchForm.submit();
}
function bidSortSel(e) {
    $("#bidSort").val(e);
    //doit
    $("#buyerName").val($("#inpBuyerName").val());
    $("#projectId").val($("#inpProjectId").val());
    $("#agentName").val($("#inpAgentName").val());
    //doit
    validateCode();
    //document.searchForm.submit();
}
function pinMuSel(e) {
    $("#pinMu").val(e);
    //doit
    $("#buyerName").val($("#inpBuyerName").val());
    $("#projectId").val($("#inpProjectId").val());
    $("#agentName").val($("#inpAgentName").val());
    //doit
    validateCode();
    //document.searchForm.submit();
}



function validateCode(e) {
if(DateDiff($("#inpCusStartTime").val(),$("#inpCusEndTime").val())>366 || DateDiff($("#inpCusStartTime").val(),$("#inpCusEndTime").val())<-366 )
    {alert("查询时间范围不能超过366天，请重新选择日期");return;}

$("#kw").val(delHtmlTag($("#kw").val()));
$("#inpBuyerName").val(delHtmlTag($("#inpBuyerName").val()));
$("#inpProjectId").val(delHtmlTag($("#inpProjectId").val()));
$("#inpAgentName").val(delHtmlTag($("#inpAgentName").val()));
    dosearch(e);
}