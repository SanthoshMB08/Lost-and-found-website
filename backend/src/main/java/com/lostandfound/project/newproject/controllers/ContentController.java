package com.lostandfound.project.newproject.controllers;

import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.PostMapping;




@RestController
public class ContentController {
    @GetMapping("/getLike")
    public String GetLikes(@RequestParam String contentid) {
        return "Liked content for parameter: " + contentid;
    }
     @PostMapping("/postLike")
     public String PostLike() {
         
         
         return "Content liked successfully";

     }
         @GetMapping("/getComment")
    public String GetComments(@RequestParam String contentid) {
        return "Commented content for parameter: " + contentid;
    }
     @PostMapping("/postComment")
     public String PostComment() {
         
         return "Content commented successfully";
         
     }
    
}
