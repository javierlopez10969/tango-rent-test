<template>
  <div class="container">
    <div class="title">{{ day }} {{ month }} {{ year }} {{ time }}</div>
    <div class="days">
      <div class="filler"></div>
      <div class="filler"></div>
      <div v-for="day in week" :key="day.id">
        <div v-if="day.id == this.day" class="day current">
          {{ day.id }}
        </div>
        <div class="day" v-else>
          {{ day.id }}
        </div>
      </div>
    </div>
    <div class="content">
      <!--Hours-->
      <div v-for="(time, i) in times" :key="i">
        <div class="time" :style="{ 'grid-row': i + 1 }">{{ time.time }}</div>
      </div>
      <!--Days-->
      <div class="filler-col"></div>
      <div class="col" style="grid-column: 3"></div>
      <div class="col" style="grid-column: 4"></div>
      <div class="col" style="grid-column: 5"></div>
      <div class="col" style="grid-column: 6"></div>
      <div class="col" style="grid-column: 7"></div>
      <div class="col weekend" style="grid-column: 8"></div>
      <div class="col weekend" style="grid-column: 9"></div>
      <div
        v-for="time in times"
        :key="time.id"
        class="row"
        :style="{ 'grid-row': time.id }"
      ></div>
      <div
        v-for="date in dates"
        :key="date.id"
        :style="date.style"
        class="event"
      >
        {{ date.startTime }} - {{ date.enddTime }} {{ date.name }}
      </div>
      <div class="current-time" :style="styleTime">
        <div class="circle"></div>
      </div>
    </div>
  </div>
</template>
<script>
export default {
  name: "NewCalendar",
  props: {
    dates: Array,
  },
  data() {
    return {
      week: [],
      times: [],
      interval: null,
      time: null,
      styleTime: ``,
    };
  },
  beforeDestroy() {
    // prevent memory leak
    clearInterval(this.interval);
  },
  computed: {
    year() {
      return new Date().getFullYear();
    },
    month() {
      const monthNames = [
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December",
      ];
      const d = new Date();
      return monthNames[d.getMonth()];
    },
    day() {
      return new Date().getDate();
    },
  },
  methods: {
    getWeek() {
      var curr = new Date(); // get current date
      var first = curr.getDate() - curr.getDay(); // First day is the day of the month - the day of the week
      var last = first + 6; // last day is the first day + 6
      for (let i = first; i <= last; i++) {
        var day = new Date(curr.setDate(i)).toUTCString();
        const element = { day: day, id: i + 1 };
        this.week.push(element);
      }
    },
    //Get blocks of time of one hour
    getTimes() {
      for (var i = 0; i < 24; i++) {
        var time = i + ": 00";
        if (i < 10) {
          time = "0" + time;
        }
        this.times.push({ time: time, id: i + 1 });
      }
    },
    calculateStyle() {
      this.dates.forEach((element) => {
        const start = element.startTime;
        const end = element.enddTime;
        const days = [
          "lunes",
          "martes",
          "miercoles",
          "jueves",
          "viernes",
          "sabado",
          "domingo",
        ];
        const day = days.indexOf(element.weekDay) + 3;
        const startHour = +start.split(":")[0] + 1;

        const endHour = +end.split(":")[0] + 1;
        const diffHour = endHour - startHour;
        const startMinute = +start.split(":")[1];
        const endMinute = +end.split(":")[1];
        const perTop = (startMinute * 100) / 60;
        //Calculate the duration of the event
        var diffMinute = endMinute - startMinute;
        var colorStyle = ["#49aeab", "#d7dbef"];
        var color = startHour % 3 == 0 ? colorStyle[0] : colorStyle[1];
        if (diffHour == 0) {
          var perHeight = (diffMinute * 100) / 60;
          element.style = `grid-column: ${day}; 
                          height: calc(${perHeight}% );
                          grid-row: ${startHour}; 
                          top: calc(${perTop}% );
                          background-color: ${color};
                          border-color: ${color};
                          `;
          return;
        }
        if (diffHour == 1 && diffMinute == 0) {
          var perHeight = 100;
        }
        if (diffHour == 1 && diffMinute < 0) {
          diffMinute = startMinute - endMinute;
          var perHeight = (diffMinute * 100) / 60;
        }

        element.style = `
            grid-column: ${day};
            grid-row: ${startHour} / span ${diffHour};
            height: calc(${perHeight}% );            
            top: calc(${perTop}% );
            background-color: ${color};
            border-color: ${color};
            ;
            `;
      });
    },
  },
  created() {
    this.getWeek();
    this.getTimes();
    this.calculateStyle();
    // update the time every second
    this.interval = setInterval(() => {
      // Concise way to format time according to system locale.
      // In my case this returns "3:48:00 am"
      this.time = Intl.DateTimeFormat(navigator.language, {
        hour: "numeric",
        minute: "numeric",
        second: "numeric",
      }).format();
      var d = new Date();
      var hour = d.getHours() + 1;
      var minute = d.getMinutes();
      var perDiff = (minute * 100) / 60;
      this.styleTime = `grid-row: ${hour};  top: calc(${perDiff}% );`;
    }, 1000);
  },
};
</script>

<style>
* {
  box-sizing: border-box;
}

body {
  background: #fff;
}

.container {
  width: 200%;
  display: grid;
  grid-template-rows: 3em 3em auto;
}

.title {
  background: #217346;
  text-align: center;
  display: grid;
  place-content: center;
  color: #fff;
  position: sticky;
  top: 0;
  z-index: 10;
}

.days {
  background: #f3f2f1;
  display: grid;
  place-content: center;
  text-align: center;
  grid-template-columns: 3em 10px repeat(7, 1fr);
  position: sticky;
  top: 3em;
  z-index: 10;
  border-bottom: 2px solid #dadce0;
}

.day {
  border-left: 1px solid #dadce0;
}

.content {
  display: grid;
  grid-template-columns: 3em 20px repeat(7, 1fr);
  grid-template-rows: repeat(24, 3em);
}

.time {
  grid-column: 1;
  text-align: right;
  align-self: end;
  font-size: 80%;
  position: relative;
  bottom: -1ex;
  color: #70757a;
  padding-right: 2px;
}

.col {
  border-right: 1px solid #dadce0;
  grid-row: 1 / span 24;
  grid-column: span 1;
}

.filler-col {
  grid-row: 1/-1;
  grid-column: 2;
  border-right: 1px solid #dadce0;
}

.row {
  grid-column: 2/-1;
  border-bottom: 1px solid #dadce0;
}

.event {
  border-radius: 5px;
  margin-right: 10px;
  font-weight: bold;
  font-size: 60%;
}

.weekend {
  background-color: #f1f3f4;
}

.calendar1 {
  background-color: #d7dbef;
  border-color: black;
}

.calendar2 {
  background-color: #b3e1f7;
  border-color: black;
}

.current-time {
  grid-column: 3 / span 7;
  border-top: 2px solid #ea4335;
  position: relative;
}

.circle {
  width: 12px;
  height: 12px;
  border: 1px solid #ea4335;
  border-radius: 50%;
  background: #ea4335;
  position: relative;
  top: -6px;
  left: -6px;
}

.current {
  font-weight: bold;
}
</style>
