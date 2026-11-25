
package com.cloudcapstone.ycsb;

import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import site.ycsb.ByteIterator;
import site.ycsb.DB;
import site.ycsb.DBException;
import site.ycsb.Status;
import site.ycsb.StringByteIterator;

import java.net.URI;
import java.net.URLEncoder;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.nio.charset.StandardCharsets;
import java.time.Duration;
import java.util.HashMap;
import java.util.Map;
import java.util.Set;
import java.util.Vector;

public class CloudCapstoneYcsbClient extends DB {

    private static final ObjectMapper MAPPER = new ObjectMapper();

    private HttpClient client;
    private String baseUrl;
    private String defaultTable;

    @Override
    public void init() throws DBException {
        baseUrl = getProperties().getProperty(
                "cloudcapstone.url",
                "http://localhost:8000"
        );

        defaultTable = getProperties().getProperty(
                "cloudcapstone.table",
                "ycsb"
        );

        client = HttpClient.newBuilder()
                .version(HttpClient.Version.HTTP_1_1)
                .connectTimeout(Duration.ofSeconds(5))
                .build();
    }

        @Override
        public Status insert(
                String table,
                String key,
                Map<String, ByteIterator> values
        ) {
        try {
            Map<String, String> fields = new HashMap<>();

            values.forEach((name, value) ->
                    fields.put(name, value.toString())
            );

            Map<String, Object> body = Map.of("value", fields);
            String jsonBody = MAPPER.writeValueAsString(body);

            HttpRequest request = HttpRequest.newBuilder()
                    .uri(recordUri(resolveTable(table), key))
                    .version(HttpClient.Version.HTTP_1_1)
                    .header("Content-Type", "application/json")
                    .POST(HttpRequest.BodyPublishers.ofString(
                            jsonBody,
                            StandardCharsets.UTF_8
                    ))
                    .build();

            HttpResponse<String> response = client.send(
                    request,
                    HttpResponse.BodyHandlers.ofString()
            );

            return response.statusCode() == 201
                    ? Status.OK
                    : Status.ERROR;

        } catch (Exception e) {
            return Status.ERROR;
        }
    }

    @Override
    public Status read(
            String table,
            String key,
            Set<String> fields,
            Map<String, ByteIterator> result
    ) {
        try {
            HttpRequest request = HttpRequest.newBuilder()
                    .uri(recordUri(resolveTable(table), key))
                    .GET()
                    .build();

            HttpResponse<String> response = client.send(
                    request,
                    HttpResponse.BodyHandlers.ofString()
            );

            if (response.statusCode() != 200) {
                return Status.ERROR;
            }

            Map<String, Object> record = MAPPER.readValue(
                    response.body(),
                    new TypeReference<Map<String, Object>>() {}
            );

            Object valueObject = record.get("value");

            if (!(valueObject instanceof Map<?, ?> values)) {
                return Status.ERROR;
            }

            values.forEach((name, value) -> {
                String fieldName = String.valueOf(name);

                if (fields == null || fields.contains(fieldName)) {
                    result.put(
                            fieldName,
                            new StringByteIterator(String.valueOf(value))
                    );
                }
            });

            return Status.OK;

        } catch (Exception e) {
            return Status.ERROR;
        }
    }

    @Override
    public Status update(
            String table,
            String key,
            Map<String, ByteIterator> values
    ) {
        return Status.NOT_IMPLEMENTED;
    }

    @Override
    public Status scan(
        String table,
        String startKey,
        int recordCount,
        Set<String> fields,
        Vector<HashMap<String, ByteIterator>> result
    ) {
     // The Cloud Capstone API does not support SCAN.
    return Status.NOT_IMPLEMENTED;
    }

    @Override
    public Status delete(String table, String key) {
        try {
            HttpRequest request = HttpRequest.newBuilder()
                    .uri(recordUri(resolveTable(table), key))
                    .DELETE()
                    .build();

            HttpResponse<String> response = client.send(
                    request,
                    HttpResponse.BodyHandlers.ofString()
            );

            return response.statusCode() == 204
                    ? Status.OK
                    : Status.ERROR;

        } catch (Exception e) {
            return Status.ERROR;
        }
    }

    private String resolveTable(String table) {
        return table == null || table.isBlank()
                ? defaultTable
                : table;
    }

    private URI recordUri(String table, String key) {
        return URI.create(
                baseUrl + "/v1/tables/" + encode(table)
                        + "/records/" + encode(key)
        );
    }

    private String encode(String value) {
        return URLEncoder.encode(
                value,
                StandardCharsets.UTF_8
        ).replace("+", "%20");
    }
}
