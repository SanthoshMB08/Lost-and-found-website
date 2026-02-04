package com.lostandfound.project.newproject.controllers;


import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController


public class PostController {
    @PostMapping("/post-found-item")
    public String postFoundItem() {
        return "Found item posted successfully";
    }

    @PostMapping("/post-lost-item")
    public String postLostItem() {
        return "Lost item posted successfully";
    }
}
