import streamlit as st
import streamlit.components.v1 as components


def show_clocks():

    clock_html = """
    <style>

    .clock-wrapper{
        width:100%;
        display:grid;
        grid-template-columns: repeat(5, minmax(0, 1fr));
        gap:10px;
        padding-right:10px;
        box-sizing:border-box;
        margin-top:10px;
        margin-bottom:10px;
    }

    .clock-container{
        padding:15px 8px;
        border-radius:15px;
        background-color:#0d0d0d;
        text-align:center;
        border:1px solid #333333;
    }

    .clock-time{
        font-size:22px;
        font-weight:bold;
        color:white;
        font-family:monospace;
        line-height:1.2;
    }

    .clock-ampm{
        font-size:14px;
        color:white;
        margin-top:4px;
        font-weight:bold;
    }

    .clock-zone{
        font-size:18px;
        color:white;
        margin-top:6px;
    }

    .clock-day{
        font-size:14px;
        color:white;
        margin-top:3px;
    }

    </style>

    <div class="clock-wrapper">

        <div class="clock-container">
            <div class="clock-time" id="est"></div>
            <div class="clock-ampm" id="est_ampm"></div>
            <div class="clock-zone">EST</div>
            <div class="clock-day" id="est_day"></div>
        </div>

        <div class="clock-container">
            <div class="clock-time" id="cst"></div>
            <div class="clock-ampm" id="cst_ampm"></div>
            <div class="clock-zone">CST</div>
            <div class="clock-day" id="cst_day"></div>
        </div>

        <div class="clock-container">
            <div class="clock-time" id="mst"></div>
            <div class="clock-ampm" id="mst_ampm"></div>
            <div class="clock-zone">MST</div>
            <div class="clock-day" id="mst_day"></div>
        </div>

        <div class="clock-container">
            <div class="clock-time" id="pst"></div>
            <div class="clock-ampm" id="pst_ampm"></div>
            <div class="clock-zone">PST</div>
            <div class="clock-day" id="pst_day"></div>
        </div>

        <div class="clock-container">
            <div class="clock-time" id="ist"></div>
            <div class="clock-ampm" id="ist_ampm"></div>
            <div class="clock-zone">IST</div>
            <div class="clock-day" id="ist_day"></div>
        </div>

    </div>

    <script>

    function formatTime(timeZone) {
        const formatter = new Intl.DateTimeFormat('en-US', {
            hour:'2-digit',
            minute:'2-digit',
            second:'2-digit',
            hour12:true,
            timeZone:timeZone
        });

        const parts = formatter.formatToParts(new Date());

        let time = "";
        let ampm = "";

        parts.forEach(p => {
            if (p.type === "dayPeriod") ampm = p.value;
            else time += p.value;
        });

        return { time, ampm };
    }

    function getDay(timeZone){
        return new Intl.DateTimeFormat('en-US', {
            weekday:'short',
            timeZone:timeZone
        }).format(new Date());
    }

    function updateClocks(){

        let est = formatTime('America/New_York');
        document.getElementById('est').innerHTML = est.time;
        document.getElementById('est_ampm').innerHTML = est.ampm;
        document.getElementById('est_day').innerHTML = getDay('America/New_York');

        let cst = formatTime('America/Chicago');
        document.getElementById('cst').innerHTML = cst.time;
        document.getElementById('cst_ampm').innerHTML = cst.ampm;
        document.getElementById('cst_day').innerHTML = getDay('America/Chicago');

        let mst = formatTime('America/Denver');
        document.getElementById('mst').innerHTML = mst.time;
        document.getElementById('mst_ampm').innerHTML = mst.ampm;
        document.getElementById('mst_day').innerHTML = getDay('America/Denver');

        let pst = formatTime('America/Los_Angeles');
        document.getElementById('pst').innerHTML = pst.time;
        document.getElementById('pst_ampm').innerHTML = pst.ampm;
        document.getElementById('pst_day').innerHTML = getDay('America/Los_Angeles');

        let ist = formatTime('Asia/Kolkata');
        document.getElementById('ist').innerHTML = ist.time;
        document.getElementById('ist_ampm').innerHTML = ist.ampm;
        document.getElementById('ist_day').innerHTML = getDay('Asia/Kolkata');
    }

    updateClocks();
    setInterval(updateClocks, 1000);

    </script>
    """

    components.html(clock_html, height=220)