package cn.pukka.software.util;

import java.util.HashMap;
import java.util.Map;

/**
 * Created by zenk on 3/23/16.
 */
public class MapBuilder<K, V> {
    public static <K, V> MapBuilder<K, V> newHashMap() {
        MapBuilder<K, V> b = new MapBuilder<>();
        b.map = new HashMap<>();
        return b;
    }

    public MapBuilder<K, V> put(K k, V v) {
        map.put(k, v);
        return this;
    }

    public MapBuilder<K, V> clear() {
        map.clear();
        return this;
    }

    public Map<K, V> build() {
        return map;
    }

    private Map<K, V> map;
}
