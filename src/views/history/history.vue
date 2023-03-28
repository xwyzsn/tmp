<template>
    <div class="tw-w-full tw-h-full">
        <el-table :data="tableData"> 
            <el-table-column prop="created_time" label="创建时间">

            </el-table-column>
            <el-table-column prop="order_id" label="订单号">
            </el-table-column>
            <el-table-column prop="price" label="消费">
            </el-table-column>

        </el-table>
    </div>
</template>
 
<script setup>
import { api } from '../../boot/api';
import { ref } from 'vue';
let tableData = ref([])
api('/gethistory', { method: 'GET' }).then((res) => {
    tableData.value = res.data;
    console.log(tableData.value)
})

</script> 
 
<style scoped></style>