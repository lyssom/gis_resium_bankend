package main

import (
	"fmt"
	"io"
	"math"
	"net/http"
	"os"
	"path/filepath"
	"sync"
	"sync/atomic"
	"time"
)

const (
	tileURL       = "http://webst01.is.autonavi.com/appmaptile?style=6&x=%d&y=%d&z=%d"
	outputDir     = "gd_tiles1"
	maxGoroutines = 5000 // 最大协程数量
)

var (
	sem         = make(chan struct{}, maxGoroutines) // 控制并发数量
	client      = &http.Client{}                     // 默认 HTTP 客户端支持 HTTP/2
	tileCounter int32                                // 下载计数器
	startTime   time.Time
)

// downloadTile 下载瓦片并保存到本地
func downloadTile(z, x, y int, wg *sync.WaitGroup) {
	defer wg.Done()
	sem <- struct{}{} // 获取信号
	defer func() { <-sem }()

	// 更新计数器
	total := atomic.AddInt32(&tileCounter, 1)
	if total%1000 == 0 {
		elapsed := time.Since(startTime)
		fmt.Printf("Downloaded %d tiles, elapsed time: %v\n", total, elapsed)
	}

	// 创建目录
	zoomDir := filepath.Join(outputDir, fmt.Sprintf("%d", z))
	levelDir := filepath.Join(zoomDir, fmt.Sprintf("%d", x))
	tileFile := filepath.Join(levelDir, fmt.Sprintf("%d.png", y))

	if _, err := os.Stat(tileFile); err == nil {
		// fmt.Printf("Tile %d-%d-%d already exists, skipping.\n", z, x, y)
		return
	}
	if err := os.MkdirAll(levelDir, os.ModePerm); err != nil {
		fmt.Printf("Error creating directory for tile %d-%d-%d: %v\n", z, x, y, err)
		return
	}

	url := fmt.Sprintf(tileURL, x, y, z)

	// 创建请求
	req, err := http.NewRequest("GET", url, nil)
	if err != nil {
		fmt.Printf("Error creating request for tile %d-%d-%d: %v\n", z, x, y, err)
		return
	}

	// 设置请求头
	// for key, value := range headers {
	// 	req.Header.Set(key, value)
	// }

	// 发起请求
	//	fmt.Println(req)
	resp, err := client.Do(req)
	if err != nil {
		fmt.Printf("Error downloading tile %d-%d-%d: %v\n", z, x, y, err)
		return
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		// fmt.Printf("Failed to download tile %d-%d-%d, status code: %d\n", z, x, y, resp.StatusCode)
		return
	}

	// 保存瓦片文件
	file, err := os.Create(tileFile)
	if err != nil {
		// fmt.Printf("Error creating file for tile %d-%d-%d: %v\n", z, x, y, err)
		return
	}
	defer file.Close()

	_, err = io.Copy(file, resp.Body)
	if err != nil {
		// fmt.Printf("Error saving tile %d-%d-%d: %v\n", z, x, y, err)
		return
	}

	// fmt.Printf("Downloaded tile %d-%d-%d\n", z, x, y)
}

func degreesToRadians(degrees float64) float64 {
	return degrees * math.Pi / 180.0
}

// 地理坐标转瓦片坐标的转换函数
func latLonToTile(lat, lon float64, z int) (int, int) {
	// 将经纬度转为墨卡托坐标
	x := (lon + 180.0) / 360.0 * math.Pow(2, float64(z))
	y := (1 - math.Log(math.Tan(degreesToRadians(lat))+1/math.Cos(degreesToRadians(lat)))/math.Pi) / 2 * math.Pow(2, float64(z))

	// 瓦片坐标需向下取整
	xTile := int(math.Floor(x))
	yTile := int(math.Floor(y))

	return xTile, yTile
}

func main() {
	var wg sync.WaitGroup
	startTime = time.Now()

	// 定义中国范围经纬度
	// minLat := 3.0   // 中国南部的纬度
	// maxLat := 53.0  // 中国北部的纬度
	// minLon := 73.0  // 中国西部的经度
	// maxLon := 135.0 // 中国东部的经度

	// // 设置要下载的区域
	// for z := 11; z <= 11; z++ { // Zoom levels
	// 	minX, minY := latLonToTile(minLat, minLon, z)
	// 	maxX, maxY := latLonToTile(maxLat, maxLon, z)

	// 	for x := minX; x <= maxX; x++ {
	// 		for y := maxY; y <= minY; y++ {
	// 			wg.Add(1)
	// 			go downloadTile(z, x, y, &wg)
	// 		}
	// 	}
	// }

	for z := 13; z <= 13; z++ { // Zoom levels
		for x := 0; x < (1 << z); x++ { // X coordinates
			for y := 0; y < (1 << z); y++ { // Y coordinates
				wg.Add(1)
				go downloadTile(z, x, y, &wg)
			}
		}
	}

	wg.Wait()
	fmt.Println("All tiles downloaded successfully.")
}
