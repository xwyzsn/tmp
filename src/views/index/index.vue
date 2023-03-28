<template>
    <div class="tw-h-full tw-w-full">
        <div class="tw-h-1/3 tw-grid tw-grid-cols-4 tw-items-center tw-content-center tw-gap-4">
            <div class="tw-border-4 tw-border-gray-600 tw-shadow-lg tw-rounded-lg tw-h-32">
                <el-statistic title="进行中的订单" :value="activeOrder" class="tw-m-4"></el-statistic>
            </div>
            <div class="tw-border-4 tw-border-gray-600 tw-shadow-lg tw-rounded-lg tw-h-32">
                <el-statistic title="总桌数" :value="20 - activeOrder" class="tw-m-4"></el-statistic>
            </div>
            <div class="tw-border-4 tw-border-gray-600 tw-shadow-lg tw-rounded-lg tw-h-32">
                <el-statistic title="未完成订单" :value="notfinished" class="tw-m-4"></el-statistic>
            </div>
            <div class="tw-border-4 tw-border-gray-600 tw-shadow-lg tw-rounded-lg tw-h-32">
                <el-statistic title="今日营业额" :value="money" class="tw-m-4"></el-statistic>
            </div>
        </div>
        <div class=" tw-h-px tw-my-8 tw-border-0  tw-bg-gray-200">
        </div>
        <div class="tw-w-full tw-h-full">
            <div id="heatmap" class="tw-w-full tw-h-1/2">

            </div>
            <div id="linemap" class="tw-w-full tw-h-1/2">

            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useCartStore, useOrderStore } from '../../stores/counter';
import * as echarts from 'echarts';
import { api } from "../../boot/api"
import dayjs from 'dayjs';
const cartStore = useCartStore();
const cart = cartStore.cart;
let setCart = cartStore.setCart;
const orderStore = useOrderStore();
const order = orderStore.order;
const activeOrder = ref(0);
let notfinished = ref(0);
let heamapData = ref([]);
let money = ref(0);
api.get('/gettodaydata').then((res) => {
    console.log(res.data);
    money.value = res.data;
})

api('/getallorder', { method: 'GET' }).then((res) => {
    // orderStore.setOrder(res);
    setCart(res.data);
}).then(() => {
    activeOrder.value = Object.keys(cart).length;
    for (let key of Object.keys(cart)) {
        for (let item of cart[key]) {
            if (!item.finish) {
                notfinished.value += 1;
                break;
            }
        }
    }
    // for(let key of Object.keys(order)){
    //     for(let item of order[key]){
    //         money.value += item.price*item.count;
    //     }
    // }

})

function getVirtualData(year, myChart, myChart2) {
    let d = null
    api.get('/getyeardata?' + new URLSearchParams({ year: year })).then((res) => {
        d = res.data
        const date = +echarts.time.parse(year + '-01-01');
        const end = +echarts.time.parse(year + '-12-31');
        const dayTime = 3600 * 24 * 1000;
        const data = [];
        for (let time = date; time <= end; time += dayTime) {
            let date = echarts.time.format(time, '{yyyy}-{MM}-{dd}', false);
            if (d[date] == undefined) {
                data.push([
                    date,
                    0
                ]);
            } else {
                data.push([
                    date,
                    d[date]
                ]);
            }
        }
        heamapData.value = data;
        let maxNumer = Math.max(...data.map((item) => {
            return item[1];
        }));
        console.log(maxNumer);
        let option = {
            visualMap: {
                show: false,
                min: 0,
                max: maxNumer,
            },
            title: {
                text: '销售额热力图',
                left: 'left',
                top: 'top'
            },
            color: ['#caf0f8', '#ade8f4', '#90e0ef', '#48cae4', '#00b4d8', '#0096c7', '#0077b6', '#023e8a', '#03045e'],
            gradientColor: ['#caf0f8', '#ade8f4', '#90e0ef', '#48cae4', '#00b4d8', '#0096c7', '#0077b6', '#023e8a', '#03045e'],
            calendar: {
                range: year,
                monthLabel: {
                    nameMap: ['一月', '二月', '三月', '四月', '五月', '六月', '七月', '八月', '九月', '十月', '十一月', '十二月']
                },
                dayLabel: {
                    firstDay: 1,
                    nameMap: ['周日', '周一', '周二', '周三', '周四', '周五', '周六']
                },
                yearLabel: {
                    show: false
                }
            },
            series: {
                type: 'heatmap',
                coordinateSystem: 'calendar',
                data: data
            },
            tooltip: {
                formatter: function (params) {
                    return echarts.format.formatTime('MM-dd', params.value[0]) + ': ' + params.value[1];
                }
            }
        };

        if (myChart) {
            myChart.setOption(option);
        }
        api.get('/gethistory').then(res => {
            let data = res.data
            let label = data.map((item) => {
                return dayjs(item.created_time).format('YYYY-MM-DD HH:mm');
            });
            let value = data.map((item) => {
                return item.price;
            });
            let option2 = {
                // 
                title: {
                    text: '最近100份订单销售额',
                    left: 'left'
                },
                xAxis: {
                    type: 'category',
                    data: label
                },
                yAxis: {
                    type: 'value'
                },
                series: [
                    {
                        data: value,
                        type: 'line',
                        smooth: true
                    }
                ]
            };
            if (myChart2) {
                myChart2.setOption(option2);
            }
        })

    })
}
// get this year 
let now = new Date();
let year = now.getFullYear();



onMounted(() => {
    let myChart = echarts.init(document.getElementById('heatmap'));
    let myChart2 = echarts.init(document.getElementById('linemap'));



    getVirtualData(year, myChart, myChart2)




    // option && myChart.setOption(option);

})
</script>
