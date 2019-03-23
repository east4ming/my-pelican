Title: 8种Java 内存溢出之一:Java Heap Space
Date: 2019-03-12 10:48
Category: Java
Tags: jvm, java, oom
Authors: 东风微鸣
Summary: 对于 java.lang.OutOfMemoryError: Java heap space , 最常见的原因很简单 -- 你把一个XXL号的应用放到了一个S号的Java heap space里了. 也就是说 -- 应用需要更多的Java heap space 来让它正常运行. 对于这个OutOfMemory, 其他的原因会更复杂, 通常是由于编程错误引起的.

[TOC]

## 1.1  java.lang.OutOfMemoryError: Java heap space 概述

Java 应用只允许使用有限的内存。这个限制是在应用启动的时候指定的。展开来说， Java内存分成2个不同的区域。这两个区域叫做Heap Space （堆内存）和 Permgen （Permanent Generation，即永久代）。

![java内存结构]({static}/images/java_memory.png)

这两个区的大小是在JVM启动的时候设置, 可以通过JVM参数`-Xmx` 和 `-XX:MaxPermSize`进行设置. 如果你没欧进行特别的设置, **平台指定**的默认配置会被使用.
`java.lang.OutOfMemoryError: Java heap space` 错误会在应用尝试添加更多的数据到heap space, 但是heap区没有足够的空间时触发.

需要注意的是即使**物理内存**可能有很多剩余, 但是只要JVM达到了heap size的限制, 就会抛出该错误.

## 1.2 原因

对于 `java.lang.OutOfMemoryError: Java heap space` , 最常见的原因很简单 -- 你把一个XXL号的应用放到了一个S号的Java heap space里了. 也就是说 -- 应用需要更多的Java heap space 来让它正常运行. 对于这个OutOfMemory, 其他的原因会更复杂, 通常是由于编程错误引起的:

 

- **用户/数据量出现峰值** 该应用被设计来处理一定数量的用户和一定数量的数据. 当用户数或数据量突然冲高, 并且超过了期望的阈值, 在出现峰值停止之前的正常运行时的操作触发了 ` java.lang.OutOfMemoryError: Java heap space` 错误.
- **内存泄漏** 一种特定类型的编程错误导致应用频繁消耗更多的内存. 每当应用的泄漏的功能被使用时, 它就会在Java heap space种生成一些对象. 随着时间推移, 泄漏的对象消耗了所有可用的Java heap space, 并且触发了常见的` java.lang.OutOfMemoryError: Java heap space`  错误.

## 1.3 示例

### 1.3.1 示例1

第一个例子相当简单 -- 下列的Java 代码尝试分配200万个(2M) 整数数组. 当你编译该代码, 用一个12MB大小的Java heap space (`java -Xmx12m OOM`)运行. 它会运行失败, 抛出 ` java.lang.OutOfMemoryError: Java heap space`  消息. 有13MB Java heap space, 这个程序就能正常运行...

```Java
class OOM {
  static final int SIZE=2*1024*1024;
  public static void main (String[] a) {
    int[] i = new int[SIZE]
  }
}
```

### 1.3.2 内存泄漏示例

第二个, 更现实一点的例子是内存泄漏. 在Java里, 当开发创建和使用新对象, 如: `new Integer(5)`, 他们不必自己分派内存 -- 这通过JVM来处理. 在应用生命周期种, JVM会周期性地检查内存中的哪个对象仍在使用, 哪个没有. 没有被使用的对象会被丢弃, 然后内存重新声明并重新使用. 这个过程叫做**垃圾回收**. 对应的JVM里的模块叫做**垃圾收集器**.

Java的自动内存管理机制以来与GC来周期性地查找没用的对象并移除他们. 简而言之, Java内存泄漏是这么一种场景, 一些对象应用已经不用了, 但是GC却没有检查出来. 结果就是这些没用的对象仍然无限期地存在在Java heap space 中. 如此往复, 最终触发`java.lang.OutOfMemoryError: Java heap space`错误.

构造一个满足内存泄漏定义的Java程序也相当容易:

```Java
class KeylessEntry {
  static class Key {
    Integer id;
 
    Key(Integer id) {
      this.id = id;
    }
  @Override
    public int hashCode() {
      return id.hashCode();
    }
  }
  public static void main(String[] args) {
    Map m = new HashMap();
    while (true)
      for (int i=0; i<10000, i++)
        if (!m.containsKey(new Key(i)))
          m.put(new Key(i), "Nmber:" + i);
  }
}
```

当执行上面的代码时，您可能期望它永远运行而没有任何问题，假设原始缓存解决方案只将Map扩展到10,000个元素，除此之外，HashMap中已经包含了所有键. 然而, 事实上元素会持续增加因为Key这个类没有在它的`hashCode()`种包含一个适当的`equals()`实现.

结果, 随着时间推移, 因为泄漏代码的不断的使用, "缓存"的结果会消耗大量的Java heap space. 当泄漏的内存填满了heap区的所有的可用内存, 并且垃圾收集器无法清理, 会抛出`java.lang.OutOfMemoryError: Java heap space`.

解决办法也简单 -- 添加个`equals()`方法的实现在下边, 就能很好的运行了. 但是在你最终找到这个bug之前, 你会西欧爱好相当多的脑细胞.

```Java
@Override
public boolean equals(Object o) {
  boolean response = false;
  if (o instanceof Key) {
    response = (((Key)o).id).equals(this.id);
  }
  return response;
}
```

## 1.4 解决方案

显然第一个解决方案就是 -- 当你的JVM特定资源耗尽了, 你应该增加那个资源的量. 在这个案例种: 当你的应用没有足够的Java heap space内存来正常运行, 只需要在运行JVM的时候配置并添加(或修改现有的)如下参数:
`-Xmx1024m`

上述配置会给应用1024M的Java heap space. 你可以使用`g`或者`G`(单位是GB), `m`或`M`(MB), `k`或`K`(KB). 例如下列都是设置最大Java heap space为1GB:

```
java -Xmx1073741824 com.mycompany.MyClass
java -Xmx1048576k com.mycompany.MyClass
java -Xmx1024m com.mycompany.MyClass
java -Xmx1g com.mycompany.MyClass
```

然而, 在很多案例种, 提供更多的Java heap space只是饮鸩止渴. 例如, 如果你的应用存在内存泄漏, 添加更多的heap只是延缓`java.lang.OutOfMemoryError: Java heap space`错误的出现, 并不能解决问题. 另外, 增加Java heap space也会导致GC暂停时间的增加, 从而影响你的应用的[吞吐量和延迟](https://plumbr.eu/blog/gc-impact-on-throughput-and-latency).

如果你希望解决潜在的问题, 而不是头痛医头, 联系我就是最好的方式(＠￣ー￣＠). 当然, 有几个工具适合你. **Debuggers**, **profiles**, **heap dump analyzers** -- 供你选择.

> 题外话:
> Dynatrace 也是个分析OOM问题的好工具.感兴趣的可以参考这篇文章:
> 《案例: Dynatrace分析某财险承保系统内存泄漏问题》

**喜欢我的博客吗? 打赏一杯:coffee:吧。您的支持是对我的最大鼓励～ 另外记得给我留言或订阅哦 :tada::tada::tada:**

**[点击这里打赏:point_right:]({filename}/pages/About.md)**
