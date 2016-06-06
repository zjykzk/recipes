public class IPUtils {
    public static boolean isPublicIP(Inet4Address inet4Address) {
        return !(inet4Address.isAnyLocalAddress() || inet4Address.isLinkLocalAddress() ||
                inet4Address.isLoopbackAddress() || inet4Address.isMCGlobal() ||
                inet4Address.isMCLinkLocal() || inet4Address.isMCOrgLocal() ||
                inet4Address.isMCSiteLocal() || inet4Address.isMulticastAddress() ||
                inet4Address.isSiteLocalAddress());
    }

    public static List<String> getPublicIP() throws SocketException {
        List<String> ips = new ArrayList<>(3);
        for (Enumeration<NetworkInterface> netInterfs =NetworkInterface.getNetworkInterfaces();
             netInterfs.hasMoreElements(); ) {
            NetworkInterface interf = netInterfs.nextElement();
            for (Enumeration<InetAddress> addrs = interf.getInetAddresses();
                 addrs.hasMoreElements(); ) {
                InetAddress addr = addrs.nextElement();
                if (addr instanceof Inet4Address && isPublicIP((Inet4Address) addr)) {
                    ips.add(addr.getHostAddress());
                }
            }
        }

        return ips;
    }
}
