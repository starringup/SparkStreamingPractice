package com.pidastar.controller;

import java.io.PrintWriter;
import java.util.Iterator;
import java.util.List;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;

import com.pidastar.entity.ProvinceStatistic;
import com.pidastar.repository.ProvinceStatisticRepository;

@Controller
public class ProvinceStatisticController 
{
	@Autowired ProvinceStatisticRepository repository;
	
	@RequestMapping("/visualization")
	public String Visualization()
	{
		return "index";
	}
	
	@RequestMapping("/getProvince")
	public void getProvinceStatistic(HttpServletRequest request,HttpServletResponse response)
	{
		JSONArray objects = new JSONArray();
		List<ProvinceStatistic> persons = repository.findAll();
		Iterator<ProvinceStatistic> iterator = persons.iterator();
		int sum = 0;
		while(iterator.hasNext()){
				ProvinceStatistic person = iterator.next();
				JSONObject object = new JSONObject();
				try {
					object.put("province", person.getProvince());
					sum += person.getCnt();
					object.put("cnt", person.getCnt() * 2);
					objects.put(object);
				} catch (JSONException e) {
					e.printStackTrace();
				}
		}
		try{
			response.setCharacterEncoding("UTF-8");
			response.setContentType("application/json");
			PrintWriter writer = response.getWriter();
			writer.write(objects.toString());
			writer.flush();
			writer.close();
		}catch(Exception exception){
			exception.printStackTrace();
		}
	}
}
