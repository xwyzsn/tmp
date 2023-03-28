import axios from "axios";
let api = axios.create({
    baseURL: "http://localhost:8085"});
export  {api,axios};
