import axios from "axios";

const API_URL = "http://localhost:8000/api/";

export const createUser = (userData) => {
    return axios.post(API_URL + "create_user/", userData);
    }

export const loginUser = (loginData) => {
    return axios.post(API_URL + "login/", loginData);
    }

export const logoutUser = () => {
    return axios.post(API_URL + "logout/");
    }
    
export const getUsers = () => {
    return axios.get(API_URL + "get_users/");
    }

export const checkLoginStatus = () => {
    return axios.get(API_URL + "check_login_status/");
    }

export const addFriend = (friendData) => {
    return axios.post(API_URL + "add_relationship/", friendData);
    }

    export async function getRelationships() {
        const response = await fetch(API_URL + "get_relationships/");
        if (!response.ok) {
          throw new Error('Failed to fetch relationships');
        }
        return response.json();
      }