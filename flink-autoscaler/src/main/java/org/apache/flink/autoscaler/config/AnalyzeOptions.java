package org.apache.flink.autoscaler.config;

import java.lang.reflect.Field;
import java.lang.reflect.Modifier;

import org.apache.flink.configuration.ConfigOption;
import org.apache.flink.configuration.description.HtmlFormatter;

public class AnalyzeOptions {
    public static void main(String[] args) {
        Class<?> classType;
        try {
            classType = Class.forName(args[0]);
            Field[] constants = classType.getFields();
            HtmlFormatter formatter = new HtmlFormatter();

            for (Field field : constants) {
                if (Modifier.isStatic(field.getModifiers()) && field.getType() == ConfigOption.class) {
                    try {
                        ConfigOption<?> tmp = (ConfigOption<?>) field.get(null);
                        System.out.println("key: " + tmp.key());
                        String description = formatter.format(tmp.description());
                        System.out.println("description: " + description);
                    } catch (IllegalArgumentException e) {
                        e.printStackTrace();
                    } catch (IllegalAccessException e) {
                        e.printStackTrace();
                    }
                }
            }
        } catch (ClassNotFoundException e) {
            e.printStackTrace();
        }
    }
}
