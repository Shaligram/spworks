
#define DRV_NAME    "tapif"
#define DRV_VERSION "0.1"
#define DRV_DESCRIPTION "Universal PKTIO device driver"

/* Interface Name Prefix which gets appended with digits 0,1 ... (Total length should be lesser than 16 chars) */
#define IF_NAME "tap"

/* Number of interfaces created */
#define NUM_OF_IFACE        4

#include <linux/kernel.h>
#include <linux/jiffies.h>
#include <linux/module.h>
#include <linux/interrupt.h>
#include <linux/fs.h>
#include <linux/types.h>
#include <linux/string.h>
#include <linux/socket.h>
#include <linux/errno.h>
#include <linux/fcntl.h>
#include <linux/in.h>
#include <asm/uaccess.h>
#include <asm/io.h>
#include <linux/inet.h>
#include <linux/netdevice.h>
#include <linux/etherdevice.h>
#include <linux/skbuff.h>
#include <linux/ethtool.h>
#include <net/sock.h>
#include <net/checksum.h>
#include <linux/if_ether.h> /* For the statistics structure. */
#include <linux/if_arp.h>   /* For ARPHRD_ETHER */
#include <linux/ip.h>
#include <linux/tcp.h>
#include <linux/percpu.h>
#include <net/net_namespace.h>
#define IFF_TAP  0x0002
#define MAX_TAP_QUEUES  DEFAULT_MAX_NUM_RSS_QUEUES
#define E100_WATCHDOG_PERIOD    (2 * HZ)
#define NET_NAME_UNKNOWN        0 
#define FLT_EXACT_COUNT 8
#define NCP_ETH_STATE_DOWN     3


struct priv_net {
    unsigned int numqueues;
    unsigned int flags;
    int mac_channel;
    kuid_t owner;
    kgid_t group;
    struct net_device   *dev;
};

struct my_device {
    struct net_device *netdev;
    struct priv_net    *priv;
};

struct my_device myDevices[NUM_OF_IFACE];
int create_interface(void);

/*
 * The higher levels take care of making this non-reentrant (it's
 * called with bh's disabled).
 */
static netdev_tx_t myif_xmit(struct sk_buff *skb,
                 struct net_device *dev)
{
    int len;

    skb_orphan(skb);

    /* Before queueing this packet to netif_rx(),
     * make sure dst is refcounted.
     */
    skb_dst_force(skb);

    skb->protocol = eth_type_trans(skb, dev);

    len = skb->len;
    /* This makes interface to re-transmit packets again like loopback
    if (likely(netif_rx(skb) == NET_RX_SUCCESS)) {
    }
    ****/

    return NETDEV_TX_OK;
}

static int myif_dev_open(struct net_device *dev)
{
    return 0;
}

static int myif_dev_stop(struct net_device *dev)
{
    return 0;
}

static int myif_dev_init(struct net_device *dev)
{
    return 0;
}

static const struct net_device_ops myif_ops = {
    .ndo_open      = myif_dev_open,
    .ndo_stop      = myif_dev_stop,
    .ndo_init      = myif_dev_init,
    .ndo_start_xmit= myif_xmit, 
    .ndo_set_mac_address = eth_mac_addr,
};

static int  
my_dev_get_settings(struct net_device *netdev, struct ethtool_cmd *ecmd)
{
    return 0;
}

static int  
my_dev_set_settings(struct net_device *netdev, struct ethtool_cmd *cmd)
{
    /* Not supported */
    return 0;
}

static void 
my_dev_get_drvinfo (struct net_device *netdev, struct ethtool_drvinfo *drvinfo)
{
    strncpy(drvinfo->driver, "myifdrv", 32);
    strncpy(drvinfo->version, "0.1", 32);
    strncpy(drvinfo->fw_version, "N/A", 32);
    strncpy(drvinfo->bus_info, "N/A", 32);

    return;
}

static int  
my_dev_get_regs_len(struct net_device *netdev)
{
    return 0;
}

static void
my_dev_get_regs(struct net_device *netdev, struct ethtool_regs *reg, void *p)
{
    return;
}

static void
my_dev_get_wol(struct net_device *netdev, struct ethtool_wolinfo *wolinfo)
{
    /* Not supported */
    return;
}

static int
my_dev_set_wol(struct net_device *netdev, struct ethtool_wolinfo *wolinfo)
{
    /* Not supported */
    return 0;
}

static u32
my_dev_get_msglevel(struct net_device *netdev)
{
    /* Not supported */
    return 0;
}

static void
my_dev_set_msglevel(struct net_device *netdev, u32 data)
{
    /* Not supported */
    return;
}

static int
my_dev_nway_reset(struct net_device *netdev)
{
    /* Not supported */
    return 0;
}

static int
my_dev_get_eeprom_len(struct net_device *netdev)
{
    /* Not supported */
    return 0;
}

static int
my_dev_get_eeprom(struct net_device *netdev, struct ethtool_eeprom *eeprom, u8 *p)
{
    /* Not supported */
    return 0;
}

static int
my_dev_set_eeprom(struct net_device *netdev, struct ethtool_eeprom *eeprom, u8 *p)
{
    /* Not supported */
    return 0;
}

static int  
my_dev_get_coalesce(struct net_device *netdev, struct ethtool_coalesce *coalesce)
{
    /* Not supported */
    return 0;
}

static int
my_dev_set_coalesce(struct net_device *netdev, struct ethtool_coalesce *coalesce)
{
    /* Not supported */
    return 0;
}

static void 
my_dev_get_ringparam(struct net_device *netdev, struct ethtool_ringparam *param)
{
    /* Not supported */
    return;
}

static int  
my_dev_set_ringparam(struct net_device *netdev, struct ethtool_ringparam *param)
{
    /* Not supported */
    return 0;
}

static void 
my_dev_get_pauseparam(struct net_device *netdev, struct ethtool_pauseparam *pause)
{
    return;
}

static int
my_dev_set_pauseparam(struct net_device *netdev, struct ethtool_pauseparam *param)
{
    /* Not supported */
    return 0;
}

static const struct ethtool_ops my_dev_ethtool_ops = {
    .get_settings           = my_dev_get_settings,
    .set_settings           = my_dev_set_settings,
    .get_drvinfo            = my_dev_get_drvinfo,
    .get_regs_len           = my_dev_get_regs_len,
    .get_regs               = my_dev_get_regs,
    .get_wol                = my_dev_get_wol,
    .set_wol                = my_dev_set_wol,
    .get_msglevel           = my_dev_get_msglevel,
    .set_msglevel           = my_dev_set_msglevel,
    .nway_reset             = my_dev_nway_reset,
    .get_link               = ethtool_op_get_link,
    .get_eeprom_len         = my_dev_get_eeprom_len,
    .get_eeprom             = my_dev_get_eeprom,
    .set_eeprom             = my_dev_set_eeprom,
    .get_coalesce           = my_dev_get_coalesce,
    .set_coalesce           = my_dev_set_coalesce,
    .get_ringparam          = my_dev_get_ringparam,
    .set_ringparam          = my_dev_set_ringparam,
    .get_pauseparam         = my_dev_get_pauseparam,
    .set_pauseparam         = my_dev_set_pauseparam,
};

static int __init my_init(void)
{
    int err = 0;
    create_interface();
    return err;    // Non-zero return means that the module couldn't be loaded.
}

int create_interface(void)
{
    char ifname[16];
    int i ;
    for (i=0; i < NUM_OF_IFACE; i++)
    {
        myDevices[i].netdev = alloc_etherdev (sizeof(struct priv_net));
        if(myDevices[i].netdev == NULL)
        {
            printk("Error while allocating device");
            return 0;
        }
        myDevices[i].priv = (struct priv_net *)netdev_priv(myDevices[i].netdev);
        memset(myDevices[i].priv, 0x0, sizeof(struct priv_net));
        myDevices[i].priv->dev = myDevices[i].netdev;
        snprintf(ifname, 16,"%s%d", IF_NAME, i);
        strncpy(myDevices[i].netdev->name, ifname, 16);
        /* Initialize netdev support APIs */
        myDevices[i].netdev->netdev_ops = &myif_ops;

        /* pmtu related setting*/
        myDevices[i].netdev->priv_flags &= ~IFF_XMIT_DST_RELEASE;
        myDevices[i].netdev->priv_flags &= (IFF_UP | IFF_PROMISC | IFF_UP);

        /* Initialize Ethtool support APIs */
        myDevices[i].netdev->ethtool_ops = (struct ethtool_ops *)&my_dev_ethtool_ops;

        if(register_netdev(myDevices[i].netdev))
        {
            printk("Fail to register interface");
        }
        netif_carrier_on(myDevices[i].netdev);
    }
    printk("[io_drv] Driver loaded successfully");
    return 0;
}

static void __exit my_cleanup(void)
{
    int i;
    printk(KERN_INFO "[io_drv] Cleaning up module.\n");
    for (i=0; i < NUM_OF_IFACE; i++)
    {
        unregister_netdev(myDevices[i].netdev);
        free_netdev(myDevices[i].netdev);
    }
}

module_init(my_init);
module_exit(my_cleanup);
MODULE_LICENSE("GPL");
MODULE_VERSION(DRV_VERSION);

